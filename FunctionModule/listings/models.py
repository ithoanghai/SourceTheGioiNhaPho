from __future__ import unicode_literals

import os.path
from datetime import datetime

from django.contrib.gis.geos import Point
from django.contrib.postgres.indexes import GinIndex, BTreeIndex
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _
from embed_video.fields import EmbedVideoField
from geopy import location
from location_field.models.spatial import LocationField
from pydantic.errors import Decimal
from rest_framework import serializers
from FunctionModule.accounts.models import User
from FunctionModule.cadastral.lookups import get_state_name, get_district_name, get_ward_name
from FunctionModule.realtors.models import Realtor
from . import get_house_type_short
from .choices import (TransactionType, HouseType, RegistrationType,
                      RoadType, Status, Direction, Condition, FurnishType, ParkingType, Construction, city_choices,
                      district_choices,
                      )


def get_image_path(instance, filename: str):
    return 'photos/listings/' + str(instance.listing.id) + '/' + filename


class Listing(models.Model):
    class Meta:
        verbose_name = "Bất động sản"
        verbose_name_plural = "DS Bất động sản"
        indexes = (
            # Full text search index
            GinIndex(fields=["street", "address"]),
            GinIndex(fields=["street", "code"]),
            # Search for code with like
            BTreeIndex(fields=['code']),
            # Search using IN query
            BTreeIndex(fields=['bedrooms', 'bathrooms', 'direction']),
            # Exact search
            models.Index(fields=["state", "district", "ward"]),
            models.Index(fields=["house_type", "transaction_type"]),
        )
        #ordering = ["state", "district"]

    user = models.ForeignKey(User,  on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("Người thêm BĐS"))
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name=_("Chuyên viên quản lý BĐS"))
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices,
                                        default=TransactionType.SELL, verbose_name=_("Hình thức giao dịch"))
    house_type = models.CharField(max_length=20, choices=HouseType.choices, default=HouseType.TOWN_HOUSE,
                                  verbose_name=_("Loại BĐS"))
    state = models.CharField(max_length=50, choices=city_choices, default="01", verbose_name=_("Thành phố/Tỉnh"))
    district = models.CharField(max_length=50, choices=district_choices, verbose_name=_("Quận/Huyện"))
    ward = models.CharField(max_length=50, verbose_name=_("Phường/Xã"), blank=True, null=True)
    urban_area = models.CharField(max_length=100, verbose_name=_("Khu đô thị/Khu dân cư"), blank=True, null=True)
    street = models.CharField(max_length=125, verbose_name=_("Tên đường, phố"),
                              help_text=_("Nhập tên Đường/Phố/Thôn/Xóm"), null=True)
    address = models.CharField(max_length=255, verbose_name=_("Địa chỉ đầy đủ"),
                               help_text=_("Nhập theo định dạng: Ngõ.Ngách.Hẻm.Số nhà, Khu dân cư, Phố, Quận/Huyện, Tỉnh/TP"))
    condition = models.CharField(max_length=20, choices=Condition.choices,
                                 verbose_name=_("Tình trạng BĐS"), blank=True, null=True)
    construction = models.CharField(max_length=20, choices=Construction.choices,
                                 verbose_name=_("Tình trạng xây dựng"), blank=True, null=True)
    year = models.CharField(max_length=50, verbose_name=_("Năm xây dựng và tỉ lệ sử dụng còn lại"), blank=True, null=True,
                            help_text=_("Điền năm hoàn thành xây dựng và Tỷ lệ % sử dụng còn lại"))
    road_type = models.CharField(max_length=20, choices=RoadType.choices, default=RoadType.ALLEY_CAR_TRIBIKE,
                                 verbose_name=_("Đường/Ngõ trước nhà"))
    lane_width = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                     verbose_name=_("Chiều rộng đường/ngõ (m)"))
    parking_type = models.CharField(max_length=20, choices=ParkingType.choices, blank=True,
                                    null=True, verbose_name=_("Có chỗ đỗ ô tô không?"))
    area = models.DecimalField(max_digits=10, decimal_places=1, verbose_name=_("Diện tích (m2)"))
    floors = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default="0",
                                 choices=([(i, i) for i in range(1, 50)]), verbose_name=_("Số tầng"))
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Mặt tiền (m)"), null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Giá chào (tỷ)"))
    receive_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Giá thu về (tỷ)"),
                                        blank=True, null=True)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Giá Hạ chào (tỷ)"),
                                     blank=True, null=True)
    average_price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name=_("Giá TB/m2 (triệu)"),
                                     blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Chiều dài (m)"), null=True,
                                 blank=True)
    area_real = models.DecimalField(max_digits=10, decimal_places=1, verbose_name=_("Diện tích thực tế(m2)"),
                                    null=True, blank=True)
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(1, 100)]), verbose_name=_("Số phòng ngủ"),
                                   null=True, blank=True)
    bathrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                    choices=([(i, i) for i in range(1, 100)]), verbose_name=_("Số phòng tắm"),
                                    null=True, blank=True)
    direction = models.CharField(max_length=20, blank=True, null=True, choices=Direction.choices, verbose_name=_("Hướng"))
    code = models.CharField(max_length=80, verbose_name=_("Mã BĐS (VIẾT HOA)"), help_text=_(
        "Chữ cái đầu Loại BĐS + 2 số cuối Năm Tháng + tên viết tắt Chuyên viên + Số BĐS của ĐC"),
                            default="NP2204HVH001", unique=True)
    title = models.CharField(max_length=200, verbose_name=_("Tiêu đề đăng (VIẾT HOA)"),
                             help_text=_("Gợi ý: Từ khoá + Vị trí (Đường/Phố/Khu) + Diện tích + Tiện ích + Giá + Sổ"))
    description = models.TextField(verbose_name=_("Mô tả cho khách về bất động sản"), default=" Chú ý: Tất cả thông tin được đăng bởi TGNP đều là thông tin thật, xác thực chính xác.", help_text=_(
        "Mô tả giới thiệu về BĐS "))
    salient_features = models.TextField(blank=True, null=True, verbose_name=_("Đặc điểm nổi bật"),
                                        help_text=_(
                                            "Nêu tất cả các ưu điểm nổi bật của BĐS"))
    location_advantage = models.TextField(blank=True, null=True, verbose_name=_("Ưu điểm vị trí"),
                                          help_text=_(
                                              "Mô tả ưu điểm của vị trí, gần địa điểm nổi tiếng, dễ nhớ nào, khoảng bao nhiêu phút ra trung tâm, đường chính, hồ, bến tàu, xe, sân vận động, rạp chiếu phim.."))
    furniture_design = models.TextField(blank=True, null=True, verbose_name=_("Nội thất, thiết kế"),
                                        help_text=_(
                                            "Thiết kế hiện đại, đầy đủ công năng, khung cột bê tông chắc chắn hay không, Có hay không có nội thất kèm theo, kèm theo những nội thất"))
    living_facilities = models.TextField(blank=True, null=True, verbose_name=_("Tiện ích sinh hoạt"),
                                         help_text=_(
                                             "Có bể bơi, phòng xông hơi, xem phim, thể thao, có chỗ đỗ xe hơi,..."))
    residential_community = models.TextField(blank=True, null=True, verbose_name=_("Cộng đồng dân cư"),
                                             help_text=_(
                                                 "Cộng đồng dân cư dân trí cao, văn minh, an ninh, thân thiện hay không"))
    regional_welfare = models.TextField(blank=True, null=True, verbose_name=_("An sinh khu vực"), help_text=_(
        "Gần trường mầm non, tiểu học, THCS,...Bệnh viện, Trung tâm spa, chăm sóc sức khoẻ, sắc đẹp..."))

    furnish_type = models.CharField(max_length=20, choices=FurnishType.choices, blank=True,
                                    null=True, default=FurnishType.SEMI_FURNISHED,
                                    verbose_name=_("Có kèm đồ đạc?"))
    registration_type = models.CharField(max_length=20, choices=RegistrationType.choices, default=RegistrationType.RED_PINK_BOOK,
                                         verbose_name=_("Loại chứng nhận"))
    bonus_rate = models.DecimalField(max_digits=2, decimal_places=1, verbose_name=_("Tỷ lệ trích thưởng (%)"),
                                     default="3", blank=True, null=True)
    reward = models.DecimalField(max_digits=5, decimal_places=0,
                                 verbose_name=_("Số tiền trích thưởng (triệu)"), default="100", blank=True,
                                 null=True)

    reward_person = models.CharField(max_length=100, blank=True, verbose_name=_("Tên chủ sở hữu BĐS"),
                                     help_text="Tên người chủ sở hữu BĐS. Ví dụ Nguyễn Văn A. Nếu BĐS của ĐC thì ghi tên của Chuyên viên ĐC và tên Cty")
    reward_person_mobile = models.CharField(max_length=50, blank=True, verbose_name=_("Số ĐT chủ sở hữu BĐS hoặc của Chuyên viên ĐC"),
                                            help_text="Số ĐT chủ sở hữu BĐS, ví dụ 0916286256")

    extra_data = models.TextField(verbose_name=_("Mô tả bđs của chuyên viên"), null=True, blank=True,
                                  help_text="Ghi các thông tin mô tả đầy đủ của đầu chủ về chủ nhà hoặc các yếu tố khác liên quan đến tương tác với Chuyên viên...")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SELLING,
                              verbose_name=_("Trạng thái giao dịch"))
    list_date = models.DateTimeField(default=datetime.now, verbose_name=_("Ngày đăng bán/cho thuê"))

    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                   choices=([(i, i) for i in range(1, 10)]), verbose_name=_("Thứ tự ưu tiên đăng"),
                                   null=True, blank=True, default=1)
    is_verified = models.BooleanField(default=False, verbose_name=_("ĐÃ XÁC MINH THÔNG TIN"))
    is_exclusive = models.BooleanField(default=False, verbose_name=_("THẾ GIỚI NHÀ PHỐ ĐỘC QUYỀN"))
    is_published = models.BooleanField(default=True, verbose_name=_("CHO PHÉP ĐĂNG"))

    location = LocationField(based_fields=['address'], zoom=7, null=True,
                             default=Point(105.83549388560711,20.976795401917798), verbose_name=_("Toạ độ vị trí BĐS"),
                             help_text="Nhập toạ độ hoặc chọn vị trí trên bản đồ")

    def __str__(self):
        return f'%s - %s' % (self.code, self.address)

    def save(self, *args, **kwargs):
        if not self.id and not self.address:
            self.address = f"{self.street}, {self.district_name} {self.state_name}"
        if float(self.area) > 0:
            ave = float(self.price)/float(self.area)*1000
            self.average_price = Decimal(round(ave, 4))

        super().save(*args, **kwargs)

    @property
    def main_photo(self):
        if self.listingimage_set is None:
            return './static/img/logo.svg'
        else:
            return self.listingimage_set.first()

    @property
    def photos(self):
        return self.listingimage_set.all().order_by('sort')

    @property
    def contract_photos(self):
        return self.listingimage_set.all().order_by('sort')

    @property
    def main_video(self):
        return self.listingvideo_set.first()

    @property
    def videos(self):
        return self.listingvideo_set.all()

    @property
    def lat(self):
        return self.location.y

    @property
    def long(self):
        return self.location.x

    def state_name(self):
        return get_state_name(self.state)

    def ward_name(self):
        return get_ward_name(self.district, self.ward)

    def district_name(self):
        return get_district_name(self.district)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "district": self.district,

        }

    @property
    def display_price(self):
        price = self.sale_price or self.price
        if price % 1 == 0:
            return f'{price.normalize} tỷ'
        else:
            return f'{price:.2f} tỷ'


class ListingImage(models.Model):
    class Meta:
        verbose_name = "Ảnh chụp BDS"
        verbose_name_plural = "Ảnh Bất động sản"
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name=_("ẢNH CHỤP BĐS"))
    sort = models.IntegerField(default=0, verbose_name=_("Thứ tự hiện"))
    description = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Thông tin"))
    photo = models.ImageField(upload_to=get_image_path, blank=False, verbose_name=_("Ảnh BĐS"))

    def __str__(self):
        return f'{self.listing_id}_{self.sort}__{self.photo.url}'

    @property
    def url(self):
        return self.photo.url

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        return super().delete(using, keep_parents)


class ListingVideo(models.Model):
    class Meta:
        verbose_name = "Đường dẫn video Youtube"
        verbose_name_plural = "Đường dẫn video Youtube"
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name=_("BĐS"))
    video = EmbedVideoField(blank=True, null=True, verbose_name=_("Link video"))


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        exclude = ('address','code')

    area = serializers.FloatField()
    area_real = serializers.FloatField()
    price = serializers.FloatField()
    receive_price = serializers.FloatField()
    sale_price = serializers.FloatField()
    lane_width = serializers.FloatField()

    lat = serializers.CharField()
    long = serializers.CharField()
    ward_name = serializers.CharField()
    state_name = serializers.CharField()
    district_name = serializers.CharField()
    main_photo = serializers.SerializerMethodField()
    list_date = TimestampField()
    priority = serializers.IntegerField()

    def get_main_photo(self, obj):
        photo = obj.main_photo
        if photo:
            return photo.url
        else:
            return ''


class ListingIndexSerializer(ListingSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ()


class ContractImage(models.Model):
    class Meta:
        verbose_name = "Ảnh chụp hợp đồng, sổ đỏ"
        verbose_name_plural = "Ảnh hợp đồng, sổ đỏ"
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                verbose_name=_("ẢNH HỢP ĐỒNG TRÍCH THƯỞNG & PHIẾU KHẢO SÁT BĐS"))
    sort = models.IntegerField(default=0, verbose_name=_("Thứ tự hiện"))
    description = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Thông tin"))
    photo = models.ImageField(upload_to=get_image_path, blank=False, verbose_name=_("Link Ảnh"))

    def __str__(self):
        return f'{self.listing_id}_{self.sort}__{self.photo.url}'

    @property
    def url(self):
        return self.photo.url

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        return super().delete(using, keep_parents)


class ListingHistory(models.Model):
    class Meta:
        verbose_name = "Lịch sử Bất động sản"
        verbose_name_plural = "Lịch sử bất động sản"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name=_("Bất động sản gốc"))
    user = models.ForeignKey(User,  on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("Người thêm BĐS"))
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_("Chuyên viên quản lý BĐS"))
    address = models.CharField(max_length=255, verbose_name=_("Địa chỉ đầy đủ"),
                               help_text=_("Nhập theo định dạng: Ngõ.Ngách.Hẻm.Số nhà, Khu dân cư, Phố, Quận/Huyện, Tỉnh/TP"))
    area = models.DecimalField(max_digits=10, decimal_places=1, verbose_name=_("Diện tích (m2)"))
    floors = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default="0",
                                 choices=([(i, i) for i in range(1, 50)]), verbose_name=_("Số tầng"))
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Mặt tiền (m)"), null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Giá chào (tỷ)"))
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(1, 100)]), verbose_name=_("Số phòng ngủ"),
                                   null=True, blank=True)
    bathrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                    choices=([(i, i) for i in range(1, 100)]), verbose_name=_("Số phòng tắm"),
                                    null=True, blank=True)
    reward_person = models.CharField(max_length=100, blank=True, verbose_name=_("Tên chủ sở hữu BĐS"),
                                     help_text="Tên người chủ sở hữu BĐS. Ví dụ Nguyễn Văn A. Nếu BĐS của ĐC thì ghi tên của Chuyên viên ĐC và tên Cty")
    reward_person_mobile = models.CharField(max_length=50, blank=True, verbose_name=_("Số ĐT chủ sở hữu BĐS hoặc của Chuyên viên ĐC"),
                                            help_text="Số ĐT chủ sở hữu BĐS, ví dụ 0916286256")

    extra_data = models.TextField(verbose_name=_("Mô tả bđs của chuyên viên"), null=True, blank=True,
                                  help_text="Ghi các thông tin mô tả đầy đủ của đầu chủ về chủ nhà hoặc các yếu tố khác liên quan đến tương tác với Chuyên viên...")

    warehouse = models.CharField(max_length=100, blank=True, verbose_name=_("Kho hàng"))
    list_date = models.DateTimeField(default=datetime.now, verbose_name=_("Ngày khởi tạo BĐS"))

    def __str__(self):
        return f'%s' % (self.listing)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def display_price(self):
        price = self.sale_price or self.price
        if price % 1 == 0:
            return f'{price.normalize} tỷ'
        else:
            return f'{price:.2f} tỷ'