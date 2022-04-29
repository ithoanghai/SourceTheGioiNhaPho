# Generated by Django 3.1.7 on 2021-11-08 18:30

import django.contrib.gis.geos.point
from django.db import migrations, models
import embed_video.fields
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_merge_20211109_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='address',
            field=models.CharField(help_text='Nhập theo định dạng: Ngõ.Ngách.Hẻm.Số nhà, Khu dân cư, Phố, Quận/Huyện, Tỉnh/TP', max_length=255, verbose_name='Địa chỉ đầy đủ'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, help_text='Mô tả giới thiệu về BĐS ', verbose_name='Mô tả bất động sản'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='district',
            field=models.CharField(choices=[('243', 'Vĩnh Yên'), ('244', 'Phúc Yên'), ('246', 'Lập Thạch'), ('247', 'Tam Dương'), ('248', 'Tam Đảo'), ('249', 'Bình Xuyên'), ('251', 'Yên Lạc'), ('252', 'Vĩnh Tường'), ('253', 'Sông Lô'), ('369', 'Ninh Bình'), ('370', 'Tam Điệp'), ('372', 'Nho Quan'), ('373', 'Gia Viễn'), ('374', 'Hoa Lư'), ('375', 'Yên Khánh'), ('376', 'Kim Sơn'), ('377', 'Yên Mô'), ('964', 'Cà Mau'), ('966', 'U Minh'), ('967', 'Thới Bình'), ('968', 'Trần Văn Thời'), ('969', 'Cái Nước'), ('970', 'Đầm Dơi'), ('971', 'Năm Căn'), ('972', 'Phú Tân'), ('973', 'Ngọc Hiển'), ('412', 'Vinh'), ('413', 'Cửa Lò'), ('414', 'Thái Hoà'), ('415', 'Quế Phong'), ('416', 'Quỳ Châu'), ('417', 'Kỳ Sơn'), ('418', 'Tương Dương'), ('419', 'Nghĩa Đàn'), ('420', 'Quỳ Hợp'), ('421', 'Quỳnh Lưu'), ('422', 'Con Cuông'), ('423', 'Tân Kỳ'), ('424', 'Anh Sơn'), ('425', 'Diễn Châu'), ('426', 'Yên Thành'), ('427', 'Đô Lương'), ('428', 'Thanh Chương'), ('429', 'Nghi Lộc'), ('430', 'Nam Đàn'), ('431', 'Hưng Nguyên'), ('432', 'Hoàng Mai'), ('855', 'Vĩnh Long'), ('857', 'Long Hồ'), ('858', 'Mang Thít'), ('859', 'Vũng Liêm'), ('860', 'Tam Bình'), ('861', 'Bình Minh'), ('862', 'Trà Ôn'), ('863', 'Bình Tân'), ('450', 'Đồng Hới'), ('452', 'Minh Hóa'), ('453', 'Tuyên Hóa'), ('454', 'Quảng Trạch'), ('455', 'Bố Trạch'), ('456', 'Quảng Ninh'), ('457', 'Lệ Thủy'), ('458', 'Ba Đồn'), ('303', 'Hồng Bàng'), ('304', 'Ngô Quyền'), ('305', 'Lê Chân'), ('306', 'Hải An'), ('307', 'Kiến An'), ('308', 'Đồ Sơn'), ('309', 'Dương Kinh'), ('311', 'Thuỷ Nguyên'), ('312', 'An Dương'), ('313', 'An Lão'), ('314', 'Kiến Thuỵ'), ('315', 'Tiên Lãng'), ('316', 'Vĩnh Bảo'), ('317', 'Cát Hải'), ('318', 'Bạch Long Vĩ'), ('001', 'Ba Đình'), ('002', 'Hoàn Kiếm'), ('003', 'Tây Hồ'), ('004', 'Long Biên'), ('005', 'Cầu Giấy'), ('006', 'Đống Đa'), ('007', 'Hai Bà Trưng'), ('008', 'Hoàng Mai'), ('009', 'Thanh Xuân'), ('016', 'Sóc Sơn'), ('017', 'Đông Anh'), ('018', 'Gia Lâm'), ('019', 'Nam Từ Liêm'), ('020', 'Thanh Trì'), ('021', 'Bắc Từ Liêm'), ('250', 'Mê Linh'), ('268', 'Hà Đông'), ('269', 'Sơn Tây'), ('271', 'Ba Vì'), ('272', 'Phúc Thọ'), ('273', 'Đan Phượng'), ('274', 'Hoài Đức'), ('275', 'Quốc Oai'), ('276', 'Thạch Thất'), ('277', 'Chương Mỹ'), ('278', 'Thanh Oai'), ('279', 'Thường Tín'), ('280', 'Phú Xuyên'), ('281', 'Ứng Hòa'), ('282', 'Mỹ Đức'), ('866', 'Cao Lãnh'), ('867', 'Sa Đéc'), ('868', 'Hồng Ngự'), ('869', 'Tân Hồng'), ('870', 'Hồng Ngự'), ('871', 'Tam Nông'), ('872', 'Tháp Mười'), ('873', 'Cao Lãnh'), ('874', 'Thanh Bình'), ('875', 'Lấp Vò'), ('876', 'Lai Vung'), ('877', 'Châu Thành'), ('105', 'Lai Châu'), ('106', 'Tam Đường'), ('107', 'Mường Tè'), ('108', 'Sìn Hồ'), ('109', 'Phong Thổ'), ('110', 'Than Uyên'), ('111', 'Tân Uyên'), ('112', 'Nậm Nhùn'), ('323', 'Hưng Yên'), ('325', 'Văn Lâm'), ('326', 'Văn Giang'), ('327', 'Yên Mỹ'), ('328', 'Mỹ Hào'), ('329', 'Ân Thi'), ('330', 'Khoái Châu'), ('331', 'Kim Động'), ('332', 'Tiên Lữ'), ('333', 'Phù Cừ'), ('178', 'Lạng Sơn'), ('180', 'Tràng Định'), ('181', 'Bình Gia'), ('182', 'Văn Lãng'), ('183', 'Cao Lộc'), ('184', 'Văn Quan'), ('185', 'Bắc Sơn'), ('186', 'Hữu Lũng'), ('187', 'Chi Lăng'), ('188', 'Lộc Bình'), ('189', 'Đình Lập'), ('731', 'Biên Hòa'), ('732', 'Long Khánh'), ('734', 'Tân Phú'), ('735', 'Vĩnh Cửu'), ('736', 'Định Quán'), ('737', 'Trảng Bom'), ('738', 'Thống Nhất'), ('739', 'Cẩm Mỹ'), ('740', 'Long Thành'), ('741', 'Xuân Lộc'), ('742', 'Nhơn Trạch'), ('815', 'Mỹ Tho'), ('816', 'Gò Công'), ('817', 'Cai Lậy'), ('818', 'Tân Phước'), ('819', 'Cái Bè'), ('820', 'Cai Lậy'), ('821', 'Châu Thành'), ('822', 'Chợ Gạo'), ('823', 'Gò Công Tây'), ('824', 'Gò Công Đông'), ('825', 'Tân Phú Đông'), ('555', 'Tuy Hoà'), ('557', 'Sông Cầu'), ('558', 'Đồng Xuân'), ('559', 'Tuy An'), ('560', 'Sơn Hòa'), ('561', 'Sông Hinh'), ('562', 'Tây Hoà'), ('563', 'Phú Hoà'), ('564', 'Đông Hòa'), ('132', 'Yên Bái'), ('133', 'Nghĩa Lộ'), ('135', 'Lục Yên'), ('136', 'Văn Yên'), ('137', 'Mù Căng Chải'), ('138', 'Trấn Yên'), ('139', 'Trạm Tấu'), ('140', 'Văn Chấn'), ('141', 'Yên Bình'), ('718', 'Thủ Dầu Một'), ('719', 'Bàu Bàng'), ('720', 'Dầu Tiếng'), ('721', 'Bến Cát'), ('722', 'Phú Giáo'), ('723', 'Tân Uyên'), ('724', 'Dĩ An'), ('725', 'Thuận An'), ('726', 'Bắc Tân Uyên'), ('502', 'Tam Kỳ'), ('503', 'Hội An'), ('504', 'Tây Giang'), ('505', 'Đông Giang'), ('506', 'Đại Lộc'), ('507', 'Điện Bàn'), ('508', 'Duy Xuyên'), ('509', 'Quế Sơn'), ('510', 'Nam Giang'), ('511', 'Phước Sơn'), ('512', 'Hiệp Đức'), ('513', 'Thăng Bình'), ('514', 'Tiên Phước'), ('515', 'Bắc Trà My'), ('516', 'Nam Trà My'), ('517', 'Núi Thành'), ('518', 'Phú Ninh'), ('519', 'Nông Sơn'), ('094', 'Điện Biên Phủ'), ('095', 'Mường Lay'), ('096', 'Mường Nhé'), ('097', 'Mường Chà'), ('098', 'Tủa Chùa'), ('099', 'Tuần Giáo'), ('100', 'Điện Biên'), ('101', 'Điện Biên Đông'), ('102', 'Mường Ảng'), ('103', 'Nậm Pồ'), ('608', 'Kon Tum'), ('610', 'Đắk Glei'), ('611', 'Ngọc Hồi'), ('612', 'Đắk Tô'), ('613', 'Kon Plông'), ('614', 'Kon Rẫy'), ('615', 'Đắk Hà'), ('616', 'Sa Thầy'), ('617', 'Tu Mơ Rông'), ('618', "Ia H' Drai"), ('954', 'Bạc Liêu'), ('956', 'Hồng Dân'), ('957', 'Phước Long'), ('958', 'Vĩnh Lợi'), ('959', 'Giá Rai'), ('960', 'Đông Hải'), ('961', 'Hoà Bình'), ('643', 'Buôn Ma Thuột'), ('644', 'Buôn Hồ'), ('645', "Ea H'leo"), ('646', 'Ea Súp'), ('647', 'Buôn Đôn'), ('648', "Cư M'gar"), ('649', 'Krông Búk'), ('650', 'Krông Năng'), ('651', 'Ea Kar'), ('652', "M'Đrắk"), ('653', 'Krông Bông'), ('654', 'Krông Pắc'), ('655', 'Krông A Na'), ('656', 'Lắk'), ('657', 'Cư Kuin'), ('883', 'Long Xuyên'), ('884', 'Châu Đốc'), ('886', 'An Phú'), ('887', 'Tân Châu'), ('888', 'Phú Tân'), ('889', 'Châu Phú'), ('890', 'Tịnh Biên'), ('891', 'Tri Tôn'), ('892', 'Châu Thành'), ('893', 'Chợ Mới'), ('894', 'Thoại Sơn'), ('380', 'Thanh Hóa'), ('381', 'Bỉm Sơn'), ('382', 'Sầm Sơn'), ('384', 'Mường Lát'), ('385', 'Quan Hóa'), ('386', 'Bá Thước'), ('387', 'Quan Sơn'), ('388', 'Lang Chánh'), ('389', 'Ngọc Lặc'), ('390', 'Cẩm Thủy'), ('391', 'Thạch Thành'), ('392', 'Hà Trung'), ('393', 'Vĩnh Lộc'), ('394', 'Yên Định'), ('395', 'Thọ Xuân'), ('396', 'Thường Xuân'), ('397', 'Triệu Sơn'), ('398', 'Thiệu Hóa'), ('399', 'Hoằng Hóa'), ('400', 'Hậu Lộc'), ('401', 'Nga Sơn'), ('402', 'Như Xuân'), ('403', 'Như Thanh'), ('404', 'Nông Cống'), ('405', 'Đông Sơn'), ('406', 'Quảng Xương'), ('407', 'Nghi Sơn'), ('522', 'Quảng Ngãi'), ('524', 'Bình Sơn'), ('525', 'Trà Bồng'), ('527', 'Sơn Tịnh'), ('528', 'Tư Nghĩa'), ('529', 'Sơn Hà'), ('530', 'Sơn Tây'), ('531', 'Minh Long'), ('532', 'Nghĩa Hành'), ('533', 'Mộ Đức'), ('534', 'Đức Phổ'), ('535', 'Ba Tơ'), ('536', 'Lý Sơn'), ('703', 'Tây Ninh'), ('705', 'Tân Biên'), ('706', 'Tân Châu'), ('707', 'Dương Minh Châu'), ('708', 'Châu Thành'), ('709', 'Hòa Thành'), ('710', 'Gò Dầu'), ('711', 'Bến Cầu'), ('712', 'Trảng Bàng'), ('213', 'Bắc Giang'), ('215', 'Yên Thế'), ('216', 'Tân Yên'), ('217', 'Lạng Giang'), ('218', 'Lục Nam'), ('219', 'Lục Ngạn'), ('220', 'Sơn Động'), ('221', 'Yên Dũng'), ('222', 'Việt Yên'), ('223', 'Hiệp Hòa'), ('760', '1'), ('761', '12'), ('764', 'Gò Vấp'), ('765', 'Bình Thạnh'), ('766', 'Tân Bình'), ('767', 'Tân Phú'), ('768', 'Phú Nhuận'), ('769', 'Thủ Đức'), ('770', '3'), ('771', '10'), ('772', '11'), ('773', '4'), ('774', '5'), ('775', '6'), ('776', '8'), ('777', 'Bình Tân'), ('778', '7'), ('783', 'Củ Chi'), ('784', 'Hóc Môn'), ('785', 'Bình Chánh'), ('786', 'Nhà Bè'), ('787', 'Cần Giờ'), ('582', 'Phan Rang-Tháp Chàm'), ('584', 'Bác Ái'), ('585', 'Ninh Sơn'), ('586', 'Ninh Hải'), ('587', 'Ninh Phước'), ('588', 'Thuận Bắc'), ('589', 'Thuận Nam'), ('070', 'Tuyên Quang'), ('071', 'Lâm Bình'), ('072', 'Na Hang'), ('073', 'Chiêm Hóa'), ('074', 'Hàm Yên'), ('075', 'Yên Sơn'), ('076', 'Sơn Dương'), ('116', 'Sơn La'), ('118', 'Quỳnh Nhai'), ('119', 'Thuận Châu'), ('120', 'Mường La'), ('121', 'Bắc Yên'), ('122', 'Phù Yên'), ('123', 'Mộc Châu'), ('124', 'Yên Châu'), ('125', 'Mai Sơn'), ('126', 'Sông Mã'), ('127', 'Sốp Cộp'), ('128', 'Vân Hồ'), ('356', 'Nam Định'), ('358', 'Mỹ Lộc'), ('359', 'Vụ Bản'), ('360', 'Ý Yên'), ('361', 'Nghĩa Hưng'), ('362', 'Nam Trực'), ('363', 'Trực Ninh'), ('364', 'Xuân Trường'), ('365', 'Giao Thủy'), ('366', 'Hải Hậu'), ('347', 'Phủ Lý'), ('349', 'Duy Tiên'), ('350', 'Kim Bảng'), ('351', 'Thanh Liêm'), ('352', 'Bình Lục'), ('353', 'Lý Nhân'), ('288', 'Hải Dương'), ('290', 'Chí Linh'), ('291', 'Nam Sách'), ('292', 'Kinh Môn'), ('293', 'Kim Thành'), ('294', 'Thanh Hà'), ('295', 'Cẩm Giàng'), ('296', 'Bình Giang'), ('297', 'Gia Lộc'), ('298', 'Tứ Kỳ'), ('299', 'Ninh Giang'), ('300', 'Thanh Miện'), ('747', 'Vũng Tàu'), ('748', 'Bà Rịa'), ('750', 'Châu Đức'), ('751', 'Xuyên Mộc'), ('752', 'Long Điền'), ('753', 'Đất Đỏ'), ('754', 'Phú Mỹ'), ('755', 'Côn Đảo'), ('899', 'Rạch Giá'), ('900', 'Hà Tiên'), ('902', 'Kiên Lương'), ('903', 'Hòn Đất'), ('904', 'Tân Hiệp'), ('905', 'Châu Thành'), ('906', 'Giồng Riềng'), ('907', 'Gò Quao'), ('908', 'An Biên'), ('909', 'An Minh'), ('910', 'Vĩnh Thuận'), ('911', 'Phú Quốc'), ('912', 'Kiên Hải'), ('913', 'U Minh Thượng'), ('914', 'Giang Thành'), ('040', 'Cao Bằng'), ('042', 'Bảo Lâm'), ('043', 'Bảo Lạc'), ('045', 'Hà Quảng'), ('047', 'Trùng Khánh'), ('048', 'Hạ Lang'), ('049', 'Quảng Hòa'), ('051', 'Hoà An'), ('052', 'Nguyên Bình'), ('053', 'Thạch An'), ('436', 'Hà Tĩnh'), ('437', 'Hồng Lĩnh'), ('439', 'Hương Sơn'), ('440', 'Đức Thọ'), ('441', 'Vũ Quang'), ('442', 'Nghi Xuân'), ('443', 'Can Lộc'), ('444', 'Hương Khê'), ('445', 'Thạch Hà'), ('446', 'Cẩm Xuyên'), ('447', 'Kỳ Anh'), ('448', 'Lộc Hà'), ('449', 'Kỳ Anh'), ('622', 'Pleiku'), ('623', 'An Khê'), ('624', 'Ayun Pa'), ('625', 'KBang'), ('626', 'Đăk Đoa'), ('627', 'Chư Păh'), ('628', 'Ia Grai'), ('629', 'Mang Yang'), ('630', 'Kông Chro'), ('631', 'Đức Cơ'), ('632', 'Chư Prông'), ('633', 'Chư Sê'), ('634', 'Đăk Pơ'), ('635', 'Ia Pa'), ('637', 'Krông Pa'), ('638', 'Phú Thiện'), ('639', 'Chư Pưh'), ('148', 'Hòa Bình'), ('150', 'Đà Bắc'), ('152', 'Lương Sơn'), ('153', 'Kim Bôi'), ('154', 'Cao Phong'), ('155', 'Tân Lạc'), ('156', 'Mai Châu'), ('157', 'Lạc Sơn'), ('158', 'Yên Thủy'), ('159', 'Lạc Thủy'), ('941', 'Sóc Trăng'), ('942', 'Châu Thành'), ('943', 'Kế Sách'), ('944', 'Mỹ Tú'), ('945', 'Cù Lao Dung'), ('946', 'Long Phú'), ('947', 'Mỹ Xuyên'), ('948', 'Ngã Năm'), ('949', 'Thạnh Trị'), ('950', 'Vĩnh Châu'), ('951', 'Trần Đề'), ('540', 'Quy Nhơn'), ('542', 'An Lão'), ('543', 'Hoài Nhơn'), ('544', 'Hoài Ân'), ('545', 'Phù Mỹ'), ('546', 'Vĩnh Thạnh'), ('547', 'Tây Sơn'), ('548', 'Phù Cát'), ('549', 'An Nhơn'), ('550', 'Tuy Phước'), ('551', 'Vân Canh'), ('336', 'Thái Bình'), ('338', 'Quỳnh Phụ'), ('339', 'Hưng Hà'), ('340', 'Đông Hưng'), ('341', 'Thái Thụy'), ('342', 'Tiền Hải'), ('343', 'Kiến Xương'), ('344', 'Vũ Thư'), ('227', 'Việt Trì'), ('228', 'Phú Thọ'), ('230', 'Đoan Hùng'), ('231', 'Hạ Hoà'), ('232', 'Thanh Ba'), ('233', 'Phù Ninh'), ('234', 'Yên Lập'), ('235', 'Cẩm Khê'), ('236', 'Tam Nông'), ('237', 'Lâm Thao'), ('238', 'Thanh Sơn'), ('239', 'Thanh Thuỷ'), ('240', 'Tân Sơn'), ('930', 'Vị Thanh'), ('931', 'Ngã Bảy'), ('932', 'Châu Thành A'), ('933', 'Châu Thành'), ('934', 'Phụng Hiệp'), ('935', 'Vị Thuỷ'), ('936', 'Long Mỹ'), ('937', 'Long Mỹ'), ('916', 'Ninh Kiều'), ('917', 'Ô Môn'), ('918', 'Bình Thuỷ'), ('919', 'Cái Răng'), ('923', 'Thốt Nốt'), ('924', 'Vĩnh Thạnh'), ('925', 'Cờ Đỏ'), ('926', 'Phong Điền'), ('927', 'Thới Lai'), ('193', 'Hạ Long'), ('194', 'Móng Cái'), ('195', 'Cẩm Phả'), ('196', 'Uông Bí'), ('198', 'Bình Liêu'), ('199', 'Tiên Yên'), ('200', 'Đầm Hà'), ('201', 'Hải Hà'), ('202', 'Ba Chẽ'), ('203', 'Vân Đồn'), ('205', 'Đông Triều'), ('206', 'Quảng Yên'), ('207', 'Cô Tô'), ('461', 'Đông Hà'), ('462', 'Quảng Trị'), ('464', 'Vĩnh Linh'), ('465', 'Hướng Hóa'), ('466', 'Gio Linh'), ('467', 'Đa Krông'), ('468', 'Cam Lộ'), ('469', 'Triệu Phong'), ('470', 'Hải Lăng'), ('471', 'Cồn Cỏ'), ('080', 'Lào Cai'), ('082', 'Bát Xát'), ('083', 'Mường Khương'), ('084', 'Si Ma Cai'), ('085', 'Bắc Hà'), ('086', 'Bảo Thắng'), ('087', 'Bảo Yên'), ('088', 'Sa Pa'), ('089', 'Văn Bàn'), ('660', 'Gia Nghĩa'), ('661', 'Đăk Glong'), ('662', 'Cư Jút'), ('663', 'Đắk Mil'), ('664', 'Krông Nô'), ('665', 'Đắk Song'), ('666', "Đắk R'Lấp"), ('667', 'Tuy Đức'), ('256', 'Bắc Ninh'), ('258', 'Yên Phong'), ('259', 'Quế Võ'), ('260', 'Tiên Du'), ('261', 'Từ Sơn'), ('262', 'Thuận Thành'), ('263', 'Gia Bình'), ('264', 'Lương Tài'), ('672', 'Đà Lạt'), ('673', 'Bảo Lộc'), ('674', 'Đam Rông'), ('675', 'Lạc Dương'), ('676', 'Lâm Hà'), ('677', 'Đơn Dương'), ('678', 'Đức Trọng'), ('679', 'Di Linh'), ('680', 'Bảo Lâm'), ('681', 'Đạ Huoai'), ('682', 'Đạ Tẻh'), ('683', 'Cát Tiên'), ('164', 'Thái Nguyên'), ('165', 'Sông Công'), ('167', 'Định Hóa'), ('168', 'Phú Lương'), ('169', 'Đồng Hỷ'), ('170', 'Võ Nhai'), ('171', 'Đại Từ'), ('172', 'Phổ Yên'), ('173', 'Phú Bình'), ('593', 'Phan Thiết'), ('594', 'La Gi'), ('595', 'Tuy Phong'), ('596', 'Bắc Bình'), ('597', 'Hàm Thuận Bắc'), ('598', 'Hàm Thuận Nam'), ('599', 'Tánh Linh'), ('600', 'Đức Linh'), ('601', 'Hàm Tân'), ('602', 'Phú Quí'), ('568', 'Nha Trang'), ('569', 'Cam Ranh'), ('570', 'Cam Lâm'), ('571', 'Vạn Ninh'), ('572', 'Ninh Hòa'), ('573', 'Khánh Vĩnh'), ('574', 'Diên Khánh'), ('575', 'Khánh Sơn'), ('576', 'Trường Sa'), ('829', 'Bến Tre'), ('831', 'Châu Thành'), ('832', 'Chợ Lách'), ('833', 'Mỏ Cày Nam'), ('834', 'Giồng Trôm'), ('835', 'Bình Đại'), ('836', 'Ba Tri'), ('837', 'Thạnh Phú'), ('838', 'Mỏ Cày Bắc'), ('474', 'Huế'), ('476', 'Phong Điền'), ('477', 'Quảng Điền'), ('478', 'Phú Vang'), ('479', 'Hương Thủy'), ('480', 'Hương Trà'), ('481', 'A Lưới'), ('482', 'Phú Lộc'), ('483', 'Nam Đông'), ('024', 'Hà Giang'), ('026', 'Đồng Văn'), ('027', 'Mèo Vạc'), ('028', 'Yên Minh'), ('029', 'Quản Bạ'), ('030', 'Vị Xuyên'), ('031', 'Bắc Mê'), ('032', 'Hoàng Su Phì'), ('033', 'Xín Mần'), ('034', 'Bắc Quang'), ('035', 'Quang Bình'), ('842', 'Trà Vinh'), ('844', 'Càng Long'), ('845', 'Cầu Kè'), ('846', 'Tiểu Cần'), ('847', 'Châu Thành'), ('848', 'Cầu Ngang'), ('849', 'Trà Cú'), ('850', 'Duyên Hải'), ('851', 'Duyên Hải'), ('794', 'Tân An'), ('795', 'Kiến Tường'), ('796', 'Tân Hưng'), ('797', 'Vĩnh Hưng'), ('798', 'Mộc Hóa'), ('799', 'Tân Thạnh'), ('800', 'Thạnh Hóa'), ('801', 'Đức Huệ'), ('802', 'Đức Hòa'), ('803', 'Bến Lức'), ('804', 'Thủ Thừa'), ('805', 'Tân Trụ'), ('806', 'Cần Đước'), ('807', 'Cần Giuộc'), ('808', 'Châu Thành'), ('058', 'Bắc Kạn'), ('060', 'Pác Nặm'), ('061', 'Ba Bể'), ('062', 'Ngân Sơn'), ('063', 'Bạch Thông'), ('064', 'Chợ Đồn'), ('065', 'Chợ Mới'), ('066', 'Na Rì'), ('490', 'Liên Chiểu'), ('491', 'Thanh Khê'), ('492', 'Hải Châu'), ('493', 'Sơn Trà'), ('494', 'Ngũ Hành Sơn'), ('495', 'Cẩm Lệ'), ('497', 'Hòa Vang'), ('498', 'Hoàng Sa'), ('688', 'Phước Long'), ('689', 'Đồng Xoài'), ('690', 'Bình Long'), ('691', 'Bù Gia Mập'), ('692', 'Lộc Ninh'), ('693', 'Bù Đốp'), ('694', 'Hớn Quản'), ('695', 'Đồng Phú'), ('696', 'Bù Đăng'), ('697', 'Chơn Thành'), ('698', 'Phú Riềng')], max_length=50, verbose_name='Quận/Huyện'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='house_type',
            field=models.CharField(choices=[('street_house', 'Nhà mặt phố'), ('town_house', 'Nhà trong ngõ'), ('loft_house', 'Nhà gác xép/Cấp 4'), ('shop_house', 'Cửa hàng'), ('building', 'Toà nhà'), ('building_business', 'Toà nhà kinh doanh'), ('office', 'Văn phòng'), ('office_tel', 'Văn phòng khách sạn'), ('condo_tel', 'Căn hộ khách sạn'), ('apartment', 'Căn hộ'), ('service_apartment', 'Căn hộ dịch vụ'), ('pent_house', 'Căn hộ áp mái'), ('villa', 'Biệt thự'), ('villa_rest', 'Biệt thự nghỉ dưỡng'), ('land', 'Đất nền'), ('land_business', 'Mặt bằng kinh doanh'), ('plot', 'Đất phân lô'), ('industrial_land', 'Đất công nghiệp'), ('warehouse_workshop', 'Kho xưởng'), ('other', 'Khác')], default='town_house', max_length=20, verbose_name='Loại BĐS'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(20.963142552138365, 105.82331127236745), help_text='Nhập toạ độ hoặc chọn vị trí trên bản đồ', null=True, srid=4326, verbose_name='Toạ độ vị trí BĐS'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='reward_person_mobile',
            field=models.CharField(blank=True, help_text='Số ĐT chủ sở hữu BĐS, ví dụ 0916286256', max_length=50, verbose_name='Số ĐT chủ sở hữu BĐS hoặc của Chuyên viên ĐC'),
        ),
        migrations.AlterField(
            model_name='listingvideo',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Link video'),
        ),
    ]
