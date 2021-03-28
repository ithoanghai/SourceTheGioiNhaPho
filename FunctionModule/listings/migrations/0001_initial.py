# Generated by Django 3.1.6 on 2021-03-27 03:40

import FunctionModule.listings.models
import datetime
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields
import location_field.models.spatial


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('realtors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Tên nhà')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Mã nhà')),
                ('price', models.IntegerField(verbose_name='Giá chào')),
                ('sale_price', models.IntegerField(blank=True, null=True, verbose_name='Giá Khuyến mãi')),
                ('state', models.CharField(choices=[('01', 'Hà Nội'), ('02', 'Hà Giang'), ('04', 'Cao Bằng'), ('06', 'Bắc Kạn'), ('08', 'Tuyên Quang'), ('10', 'Lào Cai'), ('11', 'Điện Biên'), ('12', 'Lai Châu'), ('14', 'Sơn La'), ('15', 'Yên Bái'), ('17', 'Hoà Bình'), ('19', 'Thái Nguyên'), ('20', 'Lạng Sơn'), ('22', 'Quảng Ninh'), ('24', 'Bắc Giang'), ('25', 'Phú Thọ'), ('26', 'Vĩnh Phúc'), ('27', 'Bắc Ninh'), ('30', 'Hải Dương'), ('31', 'Hải Phòng'), ('33', 'Hưng Yên'), ('34', 'Thái Bình'), ('35', 'Hà Nam'), ('36', 'Nam Định'), ('37', 'Ninh Bình'), ('38', 'Thanh Hóa'), ('40', 'Nghệ An'), ('42', 'Hà Tĩnh'), ('44', 'Quảng Bình'), ('45', 'Quảng Trị'), ('46', 'Thừa Thiên Huế'), ('48', 'Đà Nẵng'), ('49', 'Quảng Nam'), ('51', 'Quảng Ngãi'), ('52', 'Bình Định'), ('54', 'Phú Yên'), ('56', 'Khánh Hòa'), ('58', 'Ninh Thuận'), ('60', 'Bình Thuận'), ('62', 'Kon Tum'), ('64', 'Gia Lai'), ('66', 'Đắk Lắk'), ('67', 'Đắk Nông'), ('68', 'Lâm Đồng'), ('70', 'Bình Phước'), ('72', 'Tây Ninh'), ('74', 'Bình Dương'), ('75', 'Đồng Nai'), ('77', 'Bà Rịa - Vũng Tàu'), ('79', 'Hồ Chí Minh'), ('80', 'Long An'), ('82', 'Tiền Giang'), ('83', 'Bến Tre'), ('84', 'Trà Vinh'), ('86', 'Vĩnh Long'), ('87', 'Đồng Tháp'), ('89', 'An Giang'), ('91', 'Kiên Giang'), ('92', 'Cần Thơ'), ('93', 'Hậu Giang'), ('94', 'Sóc Trăng'), ('95', 'Bạc Liêu'), ('96', 'Cà Mau')], default='01', max_length=50, verbose_name='Thành phố/Tỉnh')),
                ('district', models.CharField(max_length=50, verbose_name='Quận/Huyện')),
                ('ward', models.CharField(blank=True, max_length=50, verbose_name='Phường/Xã')),
                ('street', models.CharField(help_text='Số nhà, ngõ, phố', max_length=125, verbose_name='Địa chỉ')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Địa chỉ đầy đủ')),
                ('location', location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(105.8401439, 21.0334474), null=True, srid=4326)),
                ('area', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Diện tích')),
                ('area_unit', models.CharField(choices=[('m2', 'm2')], default='m2', max_length=5, verbose_name='Đơn vị diện tích')),
                ('length', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Chiều dài')),
                ('width', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Chiều rộng')),
                ('direction', models.CharField(choices=[('east', 'Đông'), ('west', 'Tây'), ('south', 'Nam'), ('north', 'Bắc')], default='east', max_length=12, verbose_name='Hướng')),
                ('bedrooms', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Số phòng ngủ')),
                ('floors', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Số tầng')),
                ('bathrooms', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Diện tích phòng tắm')),
                ('lot_size', models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='Diện tích vườn')),
                ('description', models.TextField(blank=True, default='', verbose_name='Mô tả')),
                ('lane_width', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Diện tích mặt đường/ngõ')),
                ('house_type', models.CharField(choices=[('city_house', 'Nhà phố'), ('villa', 'Biệt thự'), ('land', 'Đất nền'), ('apartment', 'Chung cư'), ('project', 'Dự án')], default='city_house', max_length=20, verbose_name='Loại nhà')),
                ('registration_type', models.CharField(choices=[('red_book', 'Sổ Đỏ'), ('pink_book', 'Sổ Hồng')], default='red_book', max_length=20, verbose_name='Loại đăng ký')),
                ('road_type', models.CharField(choices=[('alley_car', 'Ngõ ô tô'), ('alley_bike', 'Ngõ xe máy'), ('street_surface', 'Mặt tiền phố')], default='street_surface', max_length=20, verbose_name='Loại mặt tiền')),
                ('is_published', models.BooleanField(default=True, verbose_name='Được phép đăng')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Đã xác minh thông tin nhà')),
                ('extra_data', models.JSONField(blank=True, default=dict, null=True, verbose_name='Thông tin khác')),
                ('list_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Ngày đăng')),
                ('realtor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Đầu chủ')),
            ],
        ),
        migrations.CreateModel(
            name='ListingVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', embed_video.fields.EmbedVideoField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(default=0, verbose_name='Thứ tự hiện')),
                ('description', models.CharField(blank=True, default='', max_length=255, verbose_name='Thông tin')),
                ('photo', models.ImageField(upload_to=FunctionModule.listings.models.get_image_path, verbose_name='Ảnh')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
        ),
    ]
