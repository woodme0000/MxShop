# -*- coding: utf-8 -*-
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class GoodsPagination(PageNumberPagination):
    """
    继承PageNumberPagination
    返回有多少页，每页多少个 ，支持每页取20个 就是 /?p=2&page_size=20
    需求:每页给X条，取出来第a页----第b页
    """
    page_size = 10
    page_size_query_param = 'page_size'  # 代表请求多少条
    page_query_param = 'page'  # 代表请求多少页 参数名字
    max_page_size = 1000
