# Generated by Django 3.1.7 on 2021-08-25 04:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0005_auto_20210824_1742'),
        ('realtors', '0003_auto_20210815_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trantype', models.CharField(choices=[('contact', 'Liên hệ'), ('oder', 'Đặt hàng'), ('buy', 'Mua'), ('sell', 'Bán'), ('rent', 'Thuê'), ('lease', 'Cho thuê'), ('intro_estate', 'Giới thiệu BĐS'), ('intro_custo', 'Giới thiệu Khách')], default='contact', max_length=25, verbose_name='Loại giao dịch')),
                ('house_type', models.CharField(blank=True, choices=[('street_house', 'Nhà mặt phố'), ('town_house', 'Nhà trong ngõ'), ('loft_house', 'Nhà gác xép/Cấp 4'), ('shop_house', 'Cửa hàng'), ('building', 'Toà nhà'), ('building_business', 'Toà nhà kinh doanh'), ('office', 'Văn phòng'), ('office_tel', 'Văn phòng khách sạn'), ('condo_tel', 'Căn hộ khách sạn'), ('apartment', 'Căn hộ'), ('service_apartment', 'Căn hộ dịch vụ'), ('pent_house', 'Căn hộ áp mái'), ('villa', 'Biệt thự'), ('villa_rest', 'Biệt thự nghỉ dưỡng'), ('land', 'Đất nền'), ('land_business', 'Mặt bằng kinh doanh'), ('plot', 'Đất phân lô'), ('industrial_land', 'Đất công nghiệp'), ('warehouse_workshop', 'Kho xưởng'), ('other', 'Khác')], max_length=20, null=True, verbose_name='Loại BĐS quan tâm')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Khu vực quan tâm')),
                ('request_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Giá kỳ vọng')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Thông điệp của khách hàng')),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='Mô tả thêm')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Thời gian phát sinh giao dịch')),
                ('status', models.CharField(choices=[('active', 'Đang giao dịch'), ('pause', 'Tạm dừng'), ('cancelTransaction', 'Huỷ'), ('completed', 'Hoàn thành')], default='active', max_length=25, verbose_name='Trạng thái giao dịch')),
                ('listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='listings.listing', verbose_name='Bất động sản')),
                ('realtor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Giao Chuyên viên quản lý')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Khách hàng')),
            ],
            options={
                'verbose_name': 'Giao dịch BĐS',
                'verbose_name_plural': 'DS Giao dịch',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('feedback', 'Trả lời khách'), ('meet', 'Dẫn khách'), ('negotiate', 'Đàm phán'), ('deposit', 'Đặt cọc'), ('cancelDeposit', 'Bỏ cọc'), ('contract', 'Ký hợp đồng'), ('cancelTransaction', 'Huỷ hợp đồng'), ('completed', 'Hoàn tất giao dịch')], default='feedback', max_length=25, verbose_name='Lý do giao dịch')),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='Diễn giải thêm')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Thời gian phát sinh giao dịch')),
                ('realtor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Chuyên viên thực hiện')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.transaction', verbose_name='Giao dịch')),
            ],
            options={
                'verbose_name': 'Lịch sử Giao dịch',
                'verbose_name_plural': 'DS Lịch sử Giao dịch',
                'ordering': ['date'],
            },
        ),
    ]
