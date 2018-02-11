from django.core import signals
from django.core.signals import request_finished
from django.core.signals import request_started
from django.core.signals import got_request_exception

from django.db.models.signals import class_prepared
from django.db.models.signals import pre_init, post_init
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_delete, post_delete
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_migrate, post_migrate

from django.test.signals import setting_changed
from django.test.signals import template_rendered

from django.db.backends.signals import connection_created
from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Tag
"""
Model signals
    pre_init                    # django的modal执行其构造方法前，自动触发
    post_init                   # django的modal执行其构造方法后，自动触发
    pre_save                    # django的modal对象保存前，自动触发
    post_save                   # django的modal对象保存后，自动触发
    pre_delete                  # django的modal对象删除前，自动触发
    post_delete                 # django的modal对象删除后，自动触发
    m2m_changed                 # django的modal中使用m2m字段操作第三张表（add,remove,clear）前后，自动触发
    class_prepared              # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发
Management signals
    pre_migrate                 # 执行migrate命令前，自动触发
    post_migrate                # 执行migrate命令后，自动触发
Request/response signals
    request_started             # 请求到来前，自动触发
    request_finished            # 请求结束后，自动触发
    got_request_exception       # 请求异常后，自动触发
Test signals
    setting_changed             # 使用test测试修改配置文件时，自动触发
    template_rendered           # 使用test测试渲染模板时，自动触发
Database Wrappers
    connection_created          # 创建数据库连接时，自动触发
"""


#def creat_tags(sender, instance=None, created=False, **kwargs)
@receiver(post_migrate)
def create_tags(sender, **kwargs):
    Tag.objects.get_or_create(name="Architecture")
    Tag.objects.get_or_create(name="Art")
    Tag.objects.get_or_create(name="Books")
    Tag.objects.get_or_create(name="Cars & Motorcycles")
    Tag.objects.get_or_create(name="DIY & Crafts")
    Tag.objects.get_or_create(name="Design")
    Tag.objects.get_or_create(name="Drink")
    Tag.objects.get_or_create(name="Education")
    Tag.objects.get_or_create(name="Fashion")
    Tag.objects.get_or_create(name="Film, Music")
    Tag.objects.get_or_create(name="Food")
    Tag.objects.get_or_create(name="Games")
    Tag.objects.get_or_create(name="Gardening")
    Tag.objects.get_or_create(name="Geeg")
    Tag.objects.get_or_create(name="Hair & beauty")
    Tag.objects.get_or_create(name="Health & fitness")
    Tag.objects.get_or_create(name="History")
    Tag.objects.get_or_create(name="Holidays & Events")
    Tag.objects.get_or_create(name="Home Decor")
    Tag.objects.get_or_create(name="Humor")
    Tag.objects.get_or_create(name="Illustrations")
    Tag.objects.get_or_create(name="Kids")
    Tag.objects.get_or_create(name="Men")
    Tag.objects.get_or_create(name="Outdoors")
    Tag.objects.get_or_create(name="Photography")
    Tag.objects.get_or_create(name="Products")
    Tag.objects.get_or_create(name="Quotes")
    Tag.objects.get_or_create(name="Science a Nature")
    Tag.objects.get_or_create(name="Sports")
    Tag.objects.get_or_create(name="Technology")
    Tag.objects.get_or_create(name="Travel")
    Tag.objects.get_or_create(name="Weddings")
    Tag.objects.get_or_create(name="Women")
    Tag.objects.get_or_create(name="Videos")

