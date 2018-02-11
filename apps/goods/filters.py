# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(DjangoFilterBackend):
    """
    DjangoFilterBackend
    需求:每页给X条，取出来第a页----第b页
    """
    pass


class ProductFilter(django_filters.rest_framework.FilterSet):
    """
    自定义的商品过滤类
    """
    # name参数，被作用的models字典， lookup_expr参数:作用的行为 ，gte代表就是大于等于
    pricemin = django_filters.NumberFilter(name='market_price', lookup_expr='gte')
    # name参数，被作用的models字典， lookup_expr参数:作用的行为 ，lte代表就是大于等于
    pricemax = django_filters.NumberFilter(name='market_price', lookup_expr='lte')
    # 下面这句话意思是  在Goods的name字段中，查找包含什么的字符，忽略大小写
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    # 同一件商品可能在一级目录也可能在二级目录也可能三级目录，此时，我们需要使用自定义method来解决这个需求
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ('pricemin', 'pricemax', 'name', 'is_new', 'is_hot')
