from random import choice

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# 负责生成 token
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_payload_handler

from MxShop.settings import API_KEY
from .models import VerifyCode
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义认证后台,overrite the authenticate method()
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            """验证username或者email"""
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer
    queryset = VerifyCode.objects.all()

    def generate_code(self):
        """
        生成4位数字的验证码
        :return: 四位的验证码
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 调用serializer的 is_valid,出错直接raise异常信息
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data可以取出来serializer里面的数据，是一个dict形式
        mobile = serializer.validated_data["mobile"]
        code = self.generate_code()

        yun_pian = YunPian(API_KEY)
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 把code写入数据库 VerifyCode
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            # 继续处理返回
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    用户视图
    """
    # 因为用户注册的时候,只需要使用含有序列化手机号、用户名的序列器,但用户资料却需要昵称、生日、手机性别，所以才去动态序列化
    queryset = User.objects.all()

    serializer_class = UserRegSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 动态返回不同的序列化程序，用来解决在同一个viewset里面，注册的字段和用户属性的字段不同而存在不同序列器的问题
    def get_serializer_class(self):
        """
        获取serializer序列器，默认使用ViewSet配置的selializer_class,即self.serializer_class,
        如果我们需要根据进来的请求不同,使用不同 serializations,可以重写方法
        Eg: 我们需要让管理员获取到所有的字段序列化信息,普通用户只能获取到部分字段序列化信息
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        else:
            return UserDetailSerializer

    # 用户用户个人信息只能用户自己看，需要permission.IsOwnerOrReadOnly,permissions.IsAuthenticated,AllowAny
    def get_permissions(self):
        """
        返回一个当前视图需要的permissions权限列表
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action == 'create':
            return [permissions.AllowAny(), ]
        else:
            return []

    def get_queryset(self):
        """
        获取列表的处理函数，传进来的应该是一个可迭代的参数，默认是self.queryset我们宁愿使用get_queryset()方法而不是直接
        去访问self.queryset，因为在这里我们可以处理很多逻辑,但是在self.queryset只能一次获取到值，并且这些结果将缓存到所
        有后续的请求中
        当我们需要根据用户提交过来的参数来返回不同的查询集,我们应该重写这个方法
        Eg: 返回某个用户的收藏列表
        """
        queryset = User.objects.all()
        return queryset

    def get_object(self):
        """
        Returns the object the view is displaying. 返回视图显示的对象
        如果你需要提供一个非标准的查询queryset,可以重写这个方法,例如在我们的url中有多个关键字参数来搜索对象
        """
        return self.request.user

    def create(self, request, *args, **kwargs):
        """
        创建新用户,创建的时候就生成token和 name返回给前段 
        Create a User model instance or Login the User.
        知识点:
        1.在serializer的 validator(self,attrs)返回的值，在view里面可以通过serializer.validated_data取出来
        2.在serializer里面定义 a,b字段，但是可以只返回 自定义的c,d字段
        2.self.data的数是一个dict
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 需求，创建用户时，能够实现生成token，并将token放到serializer.data里面返还给客户端
        #ser_data = serializer.data

        user = serializer.save()

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 保存实例
        serializer.save()


class HandleExcelView(View):
    def get(self,request):
        return render(request,'upload_xls.html', {'msg':'爽'})

    def post(self,request):
        file_path = request.POST.get('file')
        file_sheet = request.POST.get('sheet_name')

        return render(request,'upload_xls.html',{'msg':'已经处理完了'})
