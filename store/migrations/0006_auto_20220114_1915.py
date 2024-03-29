# Generated by Django 3.2.9 on 2022-01-14 12:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20220114_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_at',
            field=models.CharField(default=datetime.datetime(2022, 1, 14, 19, 15, 25, 791570), editable=False, max_length=50, verbose_name='ngày đăng'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='order_dt',
            field=models.CharField(default=datetime.datetime(2022, 1, 14, 19, 15, 25, 791570), editable=False, max_length=50, verbose_name='ngày đặt hàng'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='total_amt',
            field=models.IntegerField(verbose_name='tổng tiền'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.IntegerField(verbose_name='giá'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.IntegerField(verbose_name='tổng tiền'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_at',
            field=models.CharField(default=datetime.datetime(2022, 1, 14, 19, 15, 25, 791570), editable=False, max_length=50, verbose_name='ngày phản hồi'),
        ),
        migrations.AlterField(
            model_name='products',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='Sản phẩm mới'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='date_added',
            field=models.CharField(default=datetime.datetime(2022, 1, 14, 19, 15, 25, 791570), editable=False, max_length=50, verbose_name='thời gian đặt'),
        ),
    ]
