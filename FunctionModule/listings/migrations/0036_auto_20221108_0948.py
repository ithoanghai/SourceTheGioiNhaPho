# Generated by Django 3.1.14 on 2022-11-08 02:48

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0035_listing_date_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractimage',
            options={'verbose_name': 'Ảnh kín bđs', 'verbose_name_plural': 'Ảnh hợp đồng, sổ đỏ,...'},
        ),
        migrations.AlterModelOptions(
            name='listinghistory',
            options={'verbose_name': 'Biến động Bất động sản', 'verbose_name_plural': 'Biến động Bất động sản'},
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Ngày lên hàng'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='priority',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Ưu tiên đăng'),
        ),
    ]
