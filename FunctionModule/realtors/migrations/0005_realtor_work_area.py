# Generated by Django 3.1.7 on 2022-05-22 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0004_auto_20220522_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtor',
            name='work_area',
            field=models.CharField(blank=True, default='Hoàng Mai, Thanh Xuân', max_length=100, null=True, verbose_name='Địa bàn khu vực Quận/Huyện hoạt động'),
        ),
    ]