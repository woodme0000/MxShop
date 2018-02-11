# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.db.models import Q
from .models import Goods, GoodsCategory, Banner, GoodsCategoryBrand, IndexAd, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    """
    三类商品分类序列化
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    二类商品分类序列化
    """
    sub_cat =CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    一类商品分类序列化
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    商品轮播图序列化
    """
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化
    """
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)   # many=True 反向序列化一般要加上

    class Meta:
        model = Goods
        fields = "__all__"


class FavGoodsSerializer(serializers.ModelSerializer):
    """
    针对用户个人中心--我的收藏,做了一个收藏商品的序列化，只返回商品的名字，店铺价格,
    """
    class Meta:
        model = Goods
        fields = ('name', 'shop_price','id')


class GoodsSerializer1(serializers.Serializer):
    """
    使用传统的Serailizer对商品序列化
    """
    click_num = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=True, max_length=300)
    goods_front_image = serializers.ImageField()

    def create(self, validated_data):
        """
        Create and return a new `Goods` instance, given the validated data.
        """
        return Goods.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Goods` instance, given the validated data.
        """
        instance.title = validated_data.get('name', instance.name)
        instance.code = validated_data.get('click_num', instance.click_num)
        instance.save()
        return instance


class BannerSerializer(serializers.ModelSerializer):
    """
    轮播的商品
    """
    class Meta:
        model = Banner
        fields = "__all__"


class BrandsSerializer(serializers.ModelSerializer):
    """
    models.GoodsCategoryBrand的序列器
    """
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    """
    首页的分类，根据首页的category一级id，展示对应的产品品牌、子栏目、对应商品, 在里面嵌套多个GoodsCategoryBrand，
    嵌套多个商品Goods
    """
    # 解决栏目里面有多个嵌套的 brands
    brands = BrandsSerializer(many=True)
    # 解决栏目里面有多个商品的问题 因为同一个商品可能在二级category下，所以得手动写
    goods = serializers.SerializerMethodField()
    # 解决栏目里面有多个嵌套的子 栏目
    sub_cat = CategorySerializer2(many=True)

    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) |
                                         Q(category__parent_category__parent_category_id=obj.id))
        goos_serializer = GoodsSerializer(all_goods, many=True)
        return goos_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
