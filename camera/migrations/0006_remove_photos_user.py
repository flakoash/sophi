# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 23:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0005_auto_20170418_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='user',
        ),
    ]
