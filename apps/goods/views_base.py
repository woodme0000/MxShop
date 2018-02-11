# -*- coding: utf-8 -*-
# goods.views_base.py

from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import Goods


class GoodsListView(View):
    """
    通过django 的view实现商品列表页
    """
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_list.append(json_dict)
        from django.http import HttpResponse
        import json
        return HttpResponse(json.dumps(json_list), content_type="application/json")
