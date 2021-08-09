# Generated by Django 3.1.7 on 2021-07-14 07:04

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
                ('transaction_type', models.CharField(choices=[('sell', 'Bán'), ('for_rent', 'Cho thuê'), ('project', 'Dự án')], default='sell', max_length=20, verbose_name='Hình thức giao dịch')),
                ('house_type', models.CharField(choices=[('street_house', 'Nhà mặt phố'), ('town_house', 'Nhà phố'), ('loft_house', 'Nhà gác xép/Cấp 4'), ('shop_house', 'Cửa hàng'), ('building', 'Toà nhà'), ('building_business', 'Toà nhà kinh doanh'), ('office', 'Văn phòng'), ('office_tel', 'Văn phòng khách sạn'), ('condo_tel', 'Căn hộ khách sạn'), ('apartment', 'Căn hộ'), ('service_apartment', 'Căn hộ dịch vụ'), ('pent_house', 'Căn hộ áp mái'), ('villa', 'Biệt thự'), ('villa_rest', 'Biệt thự nghỉ dưỡng'), ('land', 'Đất nền'), ('land_business', 'Mặt bằng kinh doanh'), ('plot', 'Đất phân lô'), ('industrial_land', 'Đất công nghiệp'), ('warehouse_workshop', 'Kho xưởng'), ('other', 'Khác')], default='town_house', max_length=20, verbose_name='Loại BĐS')),
                ('code', models.CharField(help_text='Quy tắc: Viết tắt chữ cái đầu Loại BĐS + 2 chữ số Năm + Tháng + Chữ cái đầu tên của Chuyên viên + Số BĐS của ĐC', max_length=80, unique=True, verbose_name='Mã BĐS (VIẾT HOA)')),
                ('title', models.CharField(help_text='Gợi ý: Từ khoá + Vị trí (Đường/Phố/Khu) + Diện tích + Tiện ích + Giá + Sổ', max_length=200, verbose_name='Tiêu đề đăng (VIẾT HOA)')),
                ('address', models.CharField(help_text='Ngõ.Ngách.Hẻm.Số nhà, Khu dân cư, Phố, Quận/Huyện, Tỉnh/TP', max_length=255, verbose_name='Địa chỉ đầy đủ')),
                ('urban_area', models.CharField(blank=True, max_length=100, null=True, verbose_name='Khu đô thị/Khu dân cư')),
                ('street', models.CharField(default='Nhập tên Đường/Phố/Thôn/Xóm', max_length=125, null=True, verbose_name='Tên đường, phố')),
                ('state', models.CharField(choices=[('01', 'Hà Nội'), ('02', 'Hà Giang'), ('04', 'Cao Bằng'), ('06', 'Bắc Kạn'), ('08', 'Tuyên Quang'), ('10', 'Lào Cai'), ('11', 'Điện Biên'), ('12', 'Lai Châu'), ('14', 'Sơn La'), ('15', 'Yên Bái'), ('17', 'Hoà Bình'), ('19', 'Thái Nguyên'), ('20', 'Lạng Sơn'), ('22', 'Quảng Ninh'), ('24', 'Bắc Giang'), ('25', 'Phú Thọ'), ('26', 'Vĩnh Phúc'), ('27', 'Bắc Ninh'), ('30', 'Hải Dương'), ('31', 'Hải Phòng'), ('33', 'Hưng Yên'), ('34', 'Thái Bình'), ('35', 'Hà Nam'), ('36', 'Nam Định'), ('37', 'Ninh Bình'), ('38', 'Thanh Hóa'), ('40', 'Nghệ An'), ('42', 'Hà Tĩnh'), ('44', 'Quảng Bình'), ('45', 'Quảng Trị'), ('46', 'Thừa Thiên Huế'), ('48', 'Đà Nẵng'), ('49', 'Quảng Nam'), ('51', 'Quảng Ngãi'), ('52', 'Bình Định'), ('54', 'Phú Yên'), ('56', 'Khánh Hòa'), ('58', 'Ninh Thuận'), ('60', 'Bình Thuận'), ('62', 'Kon Tum'), ('64', 'Gia Lai'), ('66', 'Đắk Lắk'), ('67', 'Đắk Nông'), ('68', 'Lâm Đồng'), ('70', 'Bình Phước'), ('72', 'Tây Ninh'), ('74', 'Bình Dương'), ('75', 'Đồng Nai'), ('77', 'Bà Rịa - Vũng Tàu'), ('79', 'Hà Nội'), ('80', 'Long An'), ('82', 'Tiền Giang'), ('83', 'Bến Tre'), ('84', 'Trà Vinh'), ('86', 'Vĩnh Long'), ('87', 'Đồng Tháp'), ('89', 'An Giang'), ('91', 'Kiên Giang'), ('92', 'Cần Thơ'), ('93', 'Hậu Giang'), ('94', 'Sóc Trăng'), ('95', 'Bạc Liêu'), ('96', 'Cà Mau')], default='01', max_length=50, verbose_name='Thành phố/Tỉnh')),
                ('district', models.CharField(default='008', max_length=50, verbose_name='Quận/Huyện')),
                ('ward', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phường/Xã')),
                ('condition', models.CharField(choices=[('new', 'Mới'), ('old', 'Cũ'), ('none', 'Chưa xác định')], default='old', max_length=20, null=True, verbose_name='Tình trạng BĐS')),
                ('year', models.CharField(blank=True, help_text='Điền năm xây dựng/Tỷ lệ % sử dụng còn lại', max_length=50, null=True, verbose_name='Năm xây dựng/Còn lại')),
                ('road_type', models.CharField(choices=[('alley_car_2', 'Ô tô tránh'), ('alley_car_tribike', 'Ô tô tránh Ba gác'), ('alley_car', 'Chỉ 1 Ô tô'), ('alley_tribike', 'Chỉ 1 Ba gác'), ('alley_tribike_bike', 'Ba gác tránh Xe máy'), ('alley_bike', 'Xe máy tránh nhau')], default='alley_car', max_length=20, verbose_name='Đường/Ngõ trước nhà')),
                ('lane_width', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Chiều rộng đường/ngõ (m)')),
                ('area', models.DecimalField(decimal_places=1, default='30', max_digits=5, verbose_name='Diện tích (m2)')),
                ('width', models.DecimalField(decimal_places=1, default='4', max_digits=5, verbose_name='Mặt tiền (m)')),
                ('length', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Chiều dài (m)')),
                ('area_real', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Diện tích thực tế(m2)')),
                ('floors', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Số tầng')),
                ('bedrooms', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)], null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Số phòng ngủ')),
                ('bathrooms', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)], null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Số phòng tắm')),
                ('direction', models.CharField(choices=[('none', 'Chưa xác định'), ('east', 'Đông'), ('south-east', 'Đông - Nam'), ('south', 'Nam'), ('south-west', 'Tây - Nam'), ('west', 'Tây'), ('north-west', 'Tây - Bắc'), ('north', 'Bắc'), ('north-east', 'Đông - Bắc')], default='none', max_length=20, verbose_name='Hướng')),
                ('description', models.TextField(blank=True, help_text='Mô tả giới thiệu BĐS ngắn gọn ', verbose_name='Mô tả ngắn gọn')),
                ('salient_features', models.TextField(blank=True, help_text='Nêu tất cả các ưu điểm nổi bật của BĐS', null=True, verbose_name='Đặc điểm nổi bật')),
                ('location_advantage', models.TextField(blank=True, help_text='Mô tả ưu điểm của vị trí, gần địa điểm nổi tiếng, dễ nhớ nào, khoảng bao nhiêu phút ra trung tâm, đường chính, hồ, bến tàu, xe, sân vận động, rạp chiếu phim..', null=True, verbose_name='Ưu điểm vị trí')),
                ('furniture_design', models.TextField(blank=True, help_text='Thiết kế hiện đại, đầy đủ công năng, khung cột bê tông chắc chắn hay không, Có hay không có nội thất kèm theo, kèm theo những nội thất', null=True, verbose_name='Nội thất, thiết kế')),
                ('living_facilities', models.TextField(blank=True, help_text='Có bể bơi, phòng xông hơi, xem phim, thể thao, có chỗ đỗ xe hơi,...', null=True, verbose_name='Tiện ích sinh hoạt')),
                ('residential_community', models.TextField(blank=True, help_text='Cộng đồng dân cư dân trí cao, văn minh, an ninh, thân thiện hay không', null=True, verbose_name='Cộng đồng dân cư')),
                ('regional_welfare', models.TextField(blank=True, help_text='Gần trường mầm non, tiểu học, THCS,...Bệnh viện, Trung tâm spa, chăm sóc sức khoẻ, sắc đẹp...', null=True, verbose_name='An sinh khu vực')),
                ('registration_type', models.CharField(blank=True, choices=[('red_book', 'Sổ Đỏ'), ('pink_book', 'Sổ Hồng'), ('dont_book', 'Chưa làm sổ')], default='red_book', max_length=20, null=True, verbose_name='Loại chứng nhận')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Giá chào (tỷ)')),
                ('receive_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Giá thu về (tỷ)')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Giá Hạ chào (tỷ)')),
                ('bonus_rate', models.DecimalField(decimal_places=1, default='3', max_digits=2, verbose_name='Tỷ lệ trích thưởng (%)')),
                ('reward', models.DecimalField(blank=True, decimal_places=0, default='100', max_digits=5, null=True, verbose_name='Số tiền trích thưởng (triệu)')),
                ('reward_person', models.CharField(blank=True, default='Nguyễn Văn A', help_text='Tên người chủ sở hữu BĐS', max_length=50, verbose_name='Tên chủ sở hữu BĐS')),
                ('reward_person_mobile', models.CharField(blank=True, default='0916286256', help_text='Số ĐT chủ sở hữu BĐS', max_length=50, verbose_name='Số ĐT chủ sở hữu BĐS')),
                ('extra_data', models.TextField(blank=True, default='Chủ nhà hiểu chuyện, tôn trọng môi giới, thiện chí hợp tác,..', help_text='Ghi các thông tin khác quan trọng về chủ nhà, các yếu tố khác liên quan...', max_length=250, null=True, verbose_name='Ghi chú')),
                ('status', models.CharField(choices=[('selling', 'Còn bán'), ('sale', 'Hạ chào'), ('sold', 'Đã bán'), ('stop_selling', 'Dừng bán')], default='selling', max_length=20, verbose_name='Trạng thái giao dịch')),
                ('is_verified', models.BooleanField(default=False, verbose_name='ĐÃ XÁC MINH THÔNG TIN')),
                ('is_exclusive', models.BooleanField(default=False, verbose_name='THẾ GIỚI NHÀ PHỐ ĐỘC QUYỀN')),
                ('is_published', models.BooleanField(default=True, verbose_name='CHO PHÉP ĐĂNG')),
                ('list_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Ngày đăng')),
                ('location', location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(105.8401439, 21.0334474), help_text='Nhập toạ độ hoặc chọn vị trí trên bản đồ', null=True, srid=4326, verbose_name='Toạ độ vị trí BĐS')),
                ('realtor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Chuyên viên')),
            ],
        ),
        migrations.CreateModel(
            name='ListingVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, null=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', verbose_name='VIDEO BĐS')),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(default=0, verbose_name='Thứ tự hiện')),
                ('description', models.CharField(blank=True, default='', max_length=255, verbose_name='Thông tin')),
                ('photo', models.ImageField(upload_to=FunctionModule.listings.models.get_image_path, verbose_name='Ảnh')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', verbose_name='ẢNH CHỤP BĐS')),
            ],
        ),
        migrations.CreateModel(
            name='ContractImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(default=0, verbose_name='Thứ tự hiện')),
                ('description', models.CharField(blank=True, default='', max_length=255, verbose_name='Thông tin')),
                ('photo', models.ImageField(upload_to=FunctionModule.listings.models.get_image_path, verbose_name='Ảnh')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', verbose_name='ẢNH HỢP ĐỒNG TRÍCH THƯỞNG & PHIẾU KHẢO SÁT BĐS')),
            ],
        ),
    ]
