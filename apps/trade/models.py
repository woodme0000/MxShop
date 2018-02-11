# -*- coding:utf-8 -*-
# trade.models.py
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model

from users.models import UserProfile
from goods.models import Goods
# Create your models here.
User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name=u'商品')
    nums = models.IntegerField(u'购买数量', default=0)
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'购物车'
        verbose_name_plural = verbose_name
        # 数据库检查，user和goods捆绑唯一性
        unique_together = ("user", "goods")

    def __str__(self):
        return "{}{}".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        ("success", '成功'),
        ("cancel", '取消'),
        ("paying", '待支付'),
    )
    PAY_TYPE = (
        ("aliapy", '支付宝'),
        ("wechat", '微信')
    )
    user = models.ForeignKey(User, verbose_name='用户')
    order_sn = models.CharField(u'订单号', unique=True, max_length=30)
    trade_no = models.CharField(u'支付宝订单号', max_length=100, unique=True, null=True, blank=True)
    pay_status = models.CharField(u'订单状态', choices=ORDER_STATUS, max_length=30, default='paying')
    post_script = models.CharField(u'订单留言', max_length=200, null=True, blank=True)
    order_mount = models.FloatField(u'订单金额', default=0.0)
    pay_time = models.DateTimeField(u'支付时间', null=True, blank=True)

    # 用户信息
    address = models.CharField(u'收获地址', default="", max_length=100)
    signer_name = models.CharField(u'签收人', default="", max_length=20)
    signer_mobile = models.CharField(u'联系电话', default="", max_length=11)

    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'订单'
        verbose_name_plural = u'订单管理'

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单里面的的商品详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name=u'订单信息', related_name='goods')
    goods = models.ForeignKey(Goods, verbose_name=u'商品信息')
    goods_num = models.IntegerField(u'商品数量', default=0)
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)


