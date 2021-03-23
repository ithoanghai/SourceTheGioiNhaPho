# Generated by Django 3.1.6 on 2021-03-22 16:38

import django.contrib.gis.geos.point
from django.db import migrations, models
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_auto_20210321_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='area',
            field=models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Diện tích'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='area_unit',
            field=models.CharField(choices=[('m2', 'm2')], default='m2', max_length=5, verbose_name='Đơn vị diện tích'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Thông tin khác'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(105.8401439, 21.0334474), null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='listing',
            name='lot_size',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='Diện tích vườn'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='state',
            field=models.CharField(choices=[('01', 'Hà Nội'), ('02', 'Hà Giang'), ('04', 'Cao Bằng'), ('06', 'Bắc Kạn'), ('08', 'Tuyên Quang'), ('10', 'Lào Cai'), ('11', 'Điện Biên'), ('12', 'Lai Châu'), ('14', 'Sơn La'), ('15', 'Yên Bái'), ('17', 'Hoà Bình'), ('19', 'Thái Nguyên'), ('20', 'Lạng Sơn'), ('22', 'Quảng Ninh'), ('24', 'Bắc Giang'), ('25', 'Phú Thọ'), ('26', 'Vĩnh Phúc'), ('27', 'Bắc Ninh'), ('30', 'Hải Dương'), ('31', 'Hải Phòng'), ('33', 'Hưng Yên'), ('34', 'Thái Bình'), ('35', 'Hà Nam'), ('36', 'Nam Định'), ('37', 'Ninh Bình'), ('38', 'Thanh Hóa'), ('40', 'Nghệ An'), ('42', 'Hà Tĩnh'), ('44', 'Quảng Bình'), ('45', 'Quảng Trị'), ('46', 'Thừa Thiên Huế'), ('48', 'Đà Nẵng'), ('49', 'Quảng Nam'), ('51', 'Quảng Ngãi'), ('52', 'Bình Định'), ('54', 'Phú Yên'), ('56', 'Khánh Hòa'), ('58', 'Ninh Thuận'), ('60', 'Bình Thuận'), ('62', 'Kon Tum'), ('64', 'Gia Lai'), ('66', 'Đắk Lắk'), ('67', 'Đắk Nông'), ('68', 'Lâm Đồng'), ('70', 'Bình Phước'), ('72', 'Tây Ninh'), ('74', 'Bình Dương'), ('75', 'Đồng Nai'), ('77', 'Bà Rịa - Vũng Tàu'), ('79', 'Hồ Chí Minh'), ('80', 'Long An'), ('82', 'Tiền Giang'), ('83', 'Bến Tre'), ('84', 'Trà Vinh'), ('86', 'Vĩnh Long'), ('87', 'Đồng Tháp'), ('89', 'An Giang'), ('91', 'Kiên Giang'), ('92', 'Cần Thơ'), ('93', 'Hậu Giang'), ('94', 'Sóc Trăng'), ('95', 'Bạc Liêu'), ('96', 'Cà Mau')], default='01', max_length=50, verbose_name='Thành phố/Tỉnh'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='street',
            field=models.CharField(help_text='Số nhà, ngõ, phố', max_length=125, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='ward',
            field=models.CharField(blank=True, max_length=50, verbose_name='Phường/Xã'),
        ),
    ]
