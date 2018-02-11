# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer, FavGoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        # 配置后，就需要user和goods组合成唯一集合组
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='这条已经收藏',  # 当出现非唯一就提示这个信息
            )
        ]
        fields = ('id', 'user', 'goods')


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    收藏详情的detail序列器，这个里面可以详细的罗列用户
    """
    goods = FavGoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('id', 'goods')


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time')


class UserAddressSerializer(serializers.ModelSerializer):
    """
    收货地址序列器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile','add_time')
