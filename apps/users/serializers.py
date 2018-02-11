# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from django.contrib.auth import get_user_model

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    发送短信验证码
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码,需要以validate开头加_ 再加变量名
        :param mobile  用户输入的手机号码
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经注册")
        # 验证手机号码正则表达式
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法!")
        # 验证发送频率
        one_mintes_ago =datetime.now() - timedelta(hours=0, minutes=1, seconds=0)  # 当前时间减去1分钟
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送时间没超过60秒")
        return mobile

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列器
    """
    # code字段: 自定义字段,不在Model里面
    code = serializers.CharField(write_only=True, required=True, max_length=4, min_length=4,
                                 error_messages={
                                     "blank": "这个字段不能为空",
                                     "required": "这个字段不能为空",
                                     "min_length": "验证码格式错误,最少需要4个",
                                     "max_length": "验证码格式错误，最多需要4个",
                                 }, help_text='验证码', label='验证码')
    # mobile字段,设置为非必填项，这样serializer将不会对mobile进行检测

    username = serializers.CharField(required=True,
                                     allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')],
                                     label="用户名")

    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='密码')

    # 序列化 用户，再进行注册的时候，需要对密码重新set 。如果直接操作密码，数据库将存储明文密码,下面代码注释是因为使用了singles策略
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        """
        验证手机号码,需要以validate开头加_ 再加变量名 时间是否>5分钟,两个验证码，以哪个为准，验证码过期
        """
        # 验证验证码是否存在,第一种方法使用get,那我们需要对异常全部捕获,用filter则不用捕获异常
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"]).order_by("add_time")
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        if verify_records:
            last_records = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=30, seconds=0)  # 验证码30分钟有效
            # last_record =12:00 30分钟后是12：30,只要当前时间是在12:30分之内，验证码都有效
            thirty_mintes_after = last_records.add_time + timedelta(hours=0, minutes=30, seconds=0)
            dd = datetime.now()
            if dd >thirty_mintes_after:
            #if five_mintes_ago < last_records.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_records.code != code:
                raise serializers.ValidationError("验证码两个不相等，错误")
        else:
            raise serializers.ValidationError("验证码真出错误")
        # 因为这个字段不会保存到数据库，所以，下面return可以注销
        return code

    # 作用在所有的serializer字段上
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列器
    """
    class Meta:
        model = User
        fields = ("name", "birthday", "gender", "email", 'mobile')
