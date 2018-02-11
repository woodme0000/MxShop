# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import HandleExcelView
urlpatterns = [
    # 商品列表页
    url(r'xls/$', HandleExcelView.as_view(), name='handle_excel'),
]