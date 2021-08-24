# Generated by Django 3.1.7 on 2021-08-15 13:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0003_auto_20210815_1839'),
        ('listings', '0004_auto_20210815_1839'),
        ('transactions', '0003_auto_20210815_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['date'], 'verbose_name': 'Giao dịch BĐS', 'verbose_name_plural': 'DS Giao dịch'},
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='code',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='price',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='reason',
        ),
        migrations.AddField(
            model_name='transaction',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Khu vực quan tâm'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='house_type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Loại BĐS quan tâm'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Thông điệp của khách hàng'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='realtor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Giao Chuyên viên quản lý'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='request_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Giá kỳ vọng'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('active', 'Đang giao dịch'), ('pause', 'Tạm dừng'), ('cancelTransaction', 'Huỷ'), ('completed', 'Hoàn thành')], default='active', max_length=25, verbose_name='Trạng thái giao dịch'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='trantype',
            field=models.CharField(choices=[('contact', 'Liên hệ'), ('oder', 'Đặt hàng'), ('buy', 'Mua'), ('sell', 'Bán'), ('rent', 'Thuê'), ('lease', 'Cho thuê'), ('intro_estate', 'Giới thiệu BĐS'), ('intro_custo', 'Giới thiệu Khách')], default='contact', max_length=25, verbose_name='Loại giao dịch'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Mô tả thêm'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Thời gian phát sinh giao dịch'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='listings.listing', verbose_name='Bất động sản'),
        ),
    ]
