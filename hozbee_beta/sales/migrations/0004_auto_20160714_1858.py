# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-14 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20160714_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundrycorder',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]