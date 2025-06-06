# Generated by Django 5.2 on 2025-06-06 03:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pickleball_platform_management', '0004_court'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Court',
            new_name='San',
        ),
        migrations.CreateModel(
            name='DanhGiaSan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diem', models.FloatField(validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('noi_dung', models.TextField()),
                ('ngay_danh_gia', models.DateTimeField(auto_now_add=True)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='danh_gias', to='pickleball_platform_management.nguoidung')),
                ('san', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='danh_gias', to='pickleball_platform_management.san')),
            ],
        ),
    ]
