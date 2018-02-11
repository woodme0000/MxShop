# -*- coding:utf-8 -*-
# 文件: goods.views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from .paginations import GoodsPagination
from .filters import GoodsFilter, ProductFilter


class CategoryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet,mixins.ListModelMixin):
    """
    http.get--list(): List all good category  \n
    http.get--retrieve(): Retrieve the pk category  \n
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer


class GoodsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    http.get--list(): List all goods, or create a new goods.User the GenericViewSet
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  # 自定义的动态Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)  # 添加自定义过滤器，系统SearchFilter
    # filter_fields = ('name', 'market_price')
    filter_class = ProductFilter
    search_fields = ('name', 'goods_desc', 'goods_brief')  # 支持搜索的字段
    ordering_fields = ('shop_price', 'sold_num', 'add_time')  # 支持按照字段进行排序

    # 被检索一次，商品点击数就+1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1  # 请求一次则click_num就+1
        instance.save()  # 保存一下
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsListView(generics.ListAPIView):
    """
    learn code, List all goods, or create a new goods.User the ListApiView
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  # 自定义的动态pagenation


class GoodsListView2(mixins.ListModelMixin, generics.GenericAPIView):
    """
    learn code ,List all goods, or create a new goods.User the GenericAPIView
    """
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


class GoodsListView1(APIView):
    """
    learn code List all goods, or create a new goods. User the APIView.
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin):
    """
    http.get--list(): List all good category  \n
    http.get--retrieve(): Retrieve the pk category  \n
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    http.get--list(): List all good category  \n
    http.get--retrieve(): Retrieve the pk category  \n
    """
    # 拿一级目录是tab的目录
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer

