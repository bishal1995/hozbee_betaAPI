# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-14 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('counpon', models.AutoField(primary_key=True, serialize=False)),
                ('counpon_code', models.CharField(db_index=True, max_length=10, unique=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('validity', models.DateField()),
                ('active', models.BooleanField(default=False)),
                ('discount_type', models.CharField(choices=[('DD', 'DIRECT_DISCOUNT'), ('PD', 'PERCENTAGE_DISCOUNT')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='CouponApplicability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('category', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=15)),
                ('level', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FoodTags',
            fields=[
                ('tag', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('tag_title', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='LaundryCatalogueItem',
            fields=[
                ('cloth', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('cloth_name', models.CharField(max_length=15)),
                ('wash_price', models.PositiveSmallIntegerField()),
                ('washService', models.CharField(choices=[('WD', 'WASH_AND_DRY'), ('WI', 'WASH_AND_IRON'), ('DW', 'DRY_WASH')], max_length=2)),
                ('clothcategory', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE'), ('H', 'HOUSEHOLD')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='TagRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UnitProduct',
            fields=[
                ('product', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('available_from', models.TimeField()),
                ('available_to', models.TimeField()),
                ('delivery', models.PositiveSmallIntegerField()),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('veg', models.BooleanField()),
                ('price', models.PositiveSmallIntegerField()),
                ('half', models.BooleanField()),
                ('half_price', models.PositiveSmallIntegerField()),
                ('thumbnail', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='BundleProduct',
            fields=[
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='products.UnitProduct')),
                ('minimun_quantity', models.PositiveSmallIntegerField()),
                ('thumbnail', models.URLField()),
            ],
        ),
    ]
