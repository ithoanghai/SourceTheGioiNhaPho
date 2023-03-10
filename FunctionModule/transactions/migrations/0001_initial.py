# Generated by Django 4.1.3 on 2022-12-07 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('realtors', '0001_initial'),
        ('customers', '0001_initial'),
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trantype', models.CharField(choices=[('contact', 'Liên hệ'), ('view', 'Liên hệ xem BĐS'), ('oder', 'Đặt hàng'), ('buy', 'Mua'), ('sell', 'Bán'), ('rent', 'Thuê'), ('lease', 'Cho thuê'), ('intro_estate', 'Giới thiệu BĐS'), ('intro_custo', 'Giới thiệu Khách')], default='contact', max_length=25, verbose_name='Loại giao dịch')),
                ('house_type', models.CharField(blank=True, choices=[('street_house', 'Nhà mặt phố'), ('town_house', 'Nhà phố'), ('loft_house', 'Nhà 1 tầng/Cấp 4'), ('shop_house', 'Cửa hàng/ShopHouse'), ('apartment', 'Căn hộ/Chung cư MN/Nhà tập thể'), ('villa', 'Biệt thự'), ('plot', 'Liền kề/Phân lô/Dịch vụ'), ('land', 'Đất nền'), ('building', 'Toà nhà'), ('building_business', 'Toà nhà kinh doanh'), ('office', 'Văn phòng'), ('office_tel', 'Văn phòng khách sạn'), ('condo_tel', 'Căn hộ khách sạn'), ('service_apartment', 'Căn hộ dịch vụ'), ('pent_house', 'Căn hộ áp mái'), ('villa_rest', 'Biệt thự nghỉ dưỡng'), ('land_business', 'Mặt bằng kinh doanh'), ('industrial_land', 'Đất công nghiệp'), ('warehouse_workshop', 'Kho xưởng'), ('other', 'Khác')], max_length=20, null=True, verbose_name='Loại BĐS quan tâm')),
                ('caring_area', models.CharField(blank=True, max_length=100, null=True, verbose_name='Khu vực quan tâm')),
                ('request_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Giá kỳ vọng/Giá chào')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Thông điệp khách hàng')),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='Mô tả')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Ngày giao dịch')),
                ('status', models.CharField(choices=[('active', 'Đang giao dịch'), ('pause', 'Tạm dừng'), ('cancelTransaction', 'Huỷ'), ('completed', 'Hoàn thành')], default='active', max_length=25, verbose_name='Trạng thái giao dịch')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='customers.customer', verbose_name='Khách hàng')),
                ('listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='listings.listing', verbose_name='Bất động sản')),
                ('realtor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='realtors.realtor', verbose_name='Chuyên viên quản lý')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
            options={
                'verbose_name': 'Giao dịch BĐS',
                'verbose_name_plural': 'Giao dịch BĐS',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('feedback', 'Trả lời khách'), ('meet', 'Dẫn khách'), ('negotiate', 'Đàm phán'), ('deposit', 'Đặt cọc'), ('cancelDeposit', 'Bỏ cọc'), ('contract', 'Ký hợp đồng'), ('cancelTransaction', 'Huỷ hợp đồng'), ('completed', 'Hoàn tất giao dịch')], default='feedback', max_length=25, verbose_name='Lý do giao dịch')),
                ('status', models.CharField(choices=[('active', 'Đang giao dịch'), ('pause', 'Tạm dừng'), ('cancelTransaction', 'Huỷ'), ('completed', 'Hoàn thành')], default='active', max_length=25, verbose_name='Trạng thái giao dịch')),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='Diễn giải')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Thời gian phản hồi')),
                ('realtor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Chuyên viên thực hiện')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transactions.transaction', verbose_name='Giao dịch')),
            ],
            options={
                'verbose_name': 'Xử lý Giao dịch',
                'verbose_name_plural': 'Xử lý Giao dịch',
                'ordering': ['date'],
            },
        ),
    ]
