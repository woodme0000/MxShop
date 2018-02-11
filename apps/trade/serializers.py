# -*- coding: utf-8 -*-
import random, time
from rest_framework import serializers

from .models import ShoppingCart, OrderInfo
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    nums = serializers.IntegerField(required=True, min_value=1, label="数量", error_messages={
        "required": "请选择购买数量",
        "min_value": "商品数量不能小于1",
    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True, label="商品")

    def create(self, validated_data):
        """
        serializer.Serializers，需要重写create()方法
        :param validated_data: python数据经过序列化，并执行is_valid()后的数据将放在validated_data
        :return: 返回当前对象的实例，ShoppingCart.instance
        """
        user = self.context["request"].user
        nums = validated_data["nums"]
        googs = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user,goods=googs)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        """
        重写update,实现更新
        :param instance: shoppingCart的实例
        :param validated_data:  serializer序列化数据验证后都放到这里
        :return: shoppingcart的实例
        """
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class ShoppingCartDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    订单序列化
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    add_time = serializers.CharField(read_only=True)

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generateordersn(self):
        nums = random.randint(10, 99)
        time_str = time.strftime("%Y%m%d%H%M%S")
        order_sn = "{time_str}{userid}{randstr}".format(time_str=time_str, userid=self.context['request'].user.id,
                                                        randstr=nums)
        print('我是订单编号:', order_sn)
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generateordersn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
