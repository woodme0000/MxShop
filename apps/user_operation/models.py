# -*- coding:utf-8 -*-
# user_operation.models.py
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods
from users.models import UserProfile
# 不管是自定义的User还是django系统的User,我们用这个方法取出来想要的
User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏功能
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserLeavingMessage(models.Model):
    """
    用户留言功能
    """
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )
    user = models.ForeignKey(User, verbose_name='用户')
    message_type = models.IntegerField(u'留言类型', default=1, choices=MESSAGE_CHOICES,
                                       help_text=u'留言类型:1(留言),'u'2(投诉),3(询问),4(售后),'u'5(求购)')
    message = models.TextField(u'留言内容', default="", help_text=u'留言内容')
    file = models.FileField(u'上传的文件', upload_to="message/images/", help_text=u'上传的文件')
    subject = models.CharField(u'主题', max_length=100, default="", help_text='文章主題')
    add_time = models.DateTimeField(u'添加时间', default=datetime.now, help_text='文章時間')

    class Meta:
        verbose_name = u'用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name='用户')
    province = models.CharField(u'省份', max_length=100, default="")
    city = models.CharField(u'城市', max_length=100, default="")
    district = models.CharField(u'区域', max_length=100, default="")
    address = models.CharField(u'详细地址', max_length=100, default="")
    signer_name = models.CharField(u'签收人', max_length=100, default="")
    signer_mobile = models.CharField(u'电话', max_length=11, default="")
    add_time = models.DateTimeField(u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
