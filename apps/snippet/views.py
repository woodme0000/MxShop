from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import status, viewsets, generics
from rest_framework.parsers import JSONParser

from snippet.models import Snippet
from snippet.serializers import SnippetSerializer, UserSerializer
from snippet.permissions import IsOwnerOrReadOnly
User = get_user_model()

# 不用进行csrf验证
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    # 删除多个对象的方法
    if request.method == 'GET':
        # 获取所有的对象
        snippets = Snippet.objects.all()
        # 序列化所有的查询集，必须设置many=True，模型对象不用设置
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        # 验证我们的数据
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# 处理单个对象的方法（get, put, delete）
# 单独对象，使用方法'GET', 'PUT', 'DELETE'（终于有用了！！！）
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
         snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # 序列化数据
        serializer = SnippetSerializer(snippet)
        data = serializer.data
        # 将数据转换成json格式，作为响应返回给客户端
        data['msg'] = '我操，为什么不能打印出去呢？'
        # json_data = JSONRenderer().render(data)
        return Response(data, status=status.HTTP_200_OK)
        # return JsonResponse(data)
        # return HttpResponse(json_data)

    elif request.method == 'PUT':
        # 将请求对象反序列化为python对象
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


class SnippetList(APIView):
    """
    这个是多个对象
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 单个对象的部分修改（APIView提供了一些request和response对象）
class SnippetDetail(APIView):
    """
    检索，更新或删除一个实例
    """
    # 首先获取对象， 发生异常就抛出404页面
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 通过重写perform_create()方法
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        (Eg. return a list of items that is specific to the user)
        """
        queryset = User.objects.all()

        return queryset
