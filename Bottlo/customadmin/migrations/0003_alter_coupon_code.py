# Generated by Django 4.2.1 on 2023-07-20 12:50

import customadmin.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0002_rename_expire_date_coupon_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default=customadmin.models.generate_coupon_code, max_length=50, unique=True),
        ),
    ]
