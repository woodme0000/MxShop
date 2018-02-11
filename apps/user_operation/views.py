# -*- coding:utf-8 -*-
# user_operation.views.py

from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer,\
    UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.


class UserFavViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """
    用户收藏功能 \n
    list:
        列出来用户的列表,使用UserFavDetailSerializer(),fields =(goods,id) \n
    create:
        创建用户的收藏列表,使用的是UserFavSerializer(), fields=(goods,users,id)  \n
    destory:
        删除用户收藏的列表,使用的是UserFavSerializer(),fields = (id,users,goods)  \n
    """
    serializer_class = UserFavSerializer
    # 增加用户是否登录的权限验证，用户未登录情况下，访问这个viewset，就会抛出一个401错误
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 添加用户认证机制，支持session认证和JSONWebToken认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    # 动态返回不同的序列化程序，用来解决在同一个viewset里面，注册的字段和用户属性的字段不同而存在不同序列器的问题
    def get_serializer_class(self):
        """
        获取serializer序列器，默认使用ViewSet配置的selializer_class,即self.serializer_class,
        如果我们需要根据进来的请求不同,使用不同 serializations,可以重写方法
        Eg: 我们需要让管理员获取到所有的字段序列化信息,普通用户只能获取到部分字段序列化信息
        """
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        else:
            return UserFavSerializer

    # 为了保证只能看到自己的收藏，需要重载我们的get_queryset(self)
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class UserLeavingMessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):
    """
    用户留言 \n
    list:
        获取用户留言 \n
    create:
        添加留言 \n
    destory:
        删除留言 \n
    """
    serializer_class = UserLeavingMessageSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    用户收货地址 \n
    list:
        获取收货冬至 \n
    create:
        添加收货地址 \n
    retrieve:
        查看收货地址 \n
    destory:
        删除收货地址 \n
    update:
        修改收货地址 \n
    """
    serializer_class = UserAddressSerializer

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
