# Generated by Django 3.1.14 on 2022-07-16 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0024_auto_20220622_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listinghistory',
            name='list_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Ngày tạo lịch sử BĐS'),
        ),
    ]