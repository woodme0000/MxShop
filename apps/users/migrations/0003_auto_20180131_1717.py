# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 17:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180124_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户管理'},
        ),
        migrations.AlterModelOptions(
            name='verifycode',
            options={'verbose_name': '短信验证码', 'verbose_name_plural': '短信验证码管理'},
        ),
    ]
