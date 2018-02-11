# -*- coding: utf-8 -*-
import xadmin

from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(object):
    # 备注：拷贝过来的代码，goods_num叫做nums，导致了报错，我将models里面的goods_num
    # 拷贝到这里
    list_display = ["user", "goods", "nums", ]


class OrderInfoAdmin(object):
    list_display = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_mount",
                    "order_mount", "pay_time", "add_time"]

    class OrderGoodsInline(object):
        model = OrderGoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderGoodsInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
