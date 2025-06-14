# Generated by Django 5.2 on 2025-06-10 00:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pickleball_platform_management', '0008_san_doanh_thu_alter_danhgiasan_noi_dung_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoidung',
            name='so_dien_thoai',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='Số điện thoại phải bắt đầu bằng 0 và có 10-11 chữ số', regex='^0\\d{9,10}$')]),
        ),
    ]
