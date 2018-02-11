# -*- coding:utf-8 -*_
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(models.Model):
    """
    商品分类，实现无限分类技能,我们用一个model实现这些功能
    """
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )

    name = models.CharField(u'商品类别', max_length=30, default="", help_text='商品类别')
    code = models.CharField(u'类别code', max_length=30, default="", help_text='类别code')
    desc = models.CharField(u'类别描述', max_length=100, default='', help_text='类别描述')
    category_type = models.IntegerField(u'类目级别', choices=CATEGORY_TYPE, help_text='类目级别')
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name='父类别',
                                        related_name='sub_cat', help_text='类别父类')
    is_tab = models.BooleanField(u'是否导航', default=False, help_text=u'是否导航')
    update_time = models.DateTimeField(u'更新时间', default=datetime.now)
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名，品牌商标
    """
    category = models.ForeignKey(GoodsCategory, related_name='brands', verbose_name=u'商品类目', null=True, blank=True)
    name = models.CharField(u'品牌名', max_length=30, default='', help_text='品牌名')
    desc = models.TextField(u'品牌描述', max_length=200, default='', help_text='品牌描述')
    image = models.ImageField(u'品牌封面', max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品信息
    """
    category = models.ForeignKey(GoodsCategory, verbose_name=u'商品类目', null=True, blank=True)
    goods_sn = models.CharField(u'商品唯一货号', max_length=50, default="")
    name = models.CharField(u'商品名称', max_length=300)
    click_num = models.IntegerField(u'点击数', default=0, null=True,blank=True)
    sold_num = models.IntegerField(u'销售量', default=0,null=True,blank=True)
    fav_num = models.IntegerField(u'收藏数', default=0, null=True,blank=True)
    goods_num = models.IntegerField(u'库存数', default=0, null=True,blank=True)
    market_price = models.FloatField(u'市场价格', default=0, null=True,blank=True)
    shop_price = models.FloatField(u'本店售价', default=0.0, null=True,blank=True)
    goods_brief = models.TextField(u'商品简短描述', max_length=500, null=True, blank=True)
    goods_desc = UEditorField(u'商品内容', imagePath='goods/images/', width=1000, height='800',
                              filePath='goods/files/', default='')  # 富文本编辑框，使用UEditorField
    ship_free = models.BooleanField(u'是否承担运费', default=True)
    goods_front_image = models.ImageField(u'封面图', upload_to="goods/images/", null=True, blank=True)
    is_new = models.BooleanField(u'是否新品', default=False)
    is_hot = models.BooleanField(u'是否热卖', default=False)

    update_time = models.DateTimeField(u'更新时间', default=datetime.now)
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name=u'商品', related_name='images')
    image = models.ImageField(u'图片', upload_to='goods/image', max_length=100, null=True,
                              blank=True)
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name='商品')
    image = models.ImageField(u'轮播图片', upload_to='banner')
    index = models.IntegerField(u"轮播顺序", default=0)
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    """
    首页商品类别广告
    """
    category = models.ForeignKey(GoodsCategory, related_name='category', verbose_name='类别')
    goods = models.ForeignKey(Goods, related_name='goods', verbose_name='商品')
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords