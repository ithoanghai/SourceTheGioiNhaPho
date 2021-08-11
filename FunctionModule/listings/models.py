from __future__ import unicode_literals

import os.path
from datetime import datetime

from django.contrib.gis.geos import Point
from django.contrib.postgres.indexes import GinIndex, BTreeIndex
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _
from embed_video.fields import EmbedVideoField
from location_field.models.spatial import LocationField
from rest_framework import serializers

from FunctionModule.cadastral.lookups import get_state_name, get_district_name, get_ward_name
from FunctionModule.realtors.models import Realtor
from .choices import (TransactionType, city_choices, HouseType, RegistrationType,
                      RoadType, Status, Direction, Condition)


def get_image_path(instance, filename: str):
    return 'photos/listings/' + str(instance.listing.id) + '/' + filename


class Listing(models.Model):
    class Meta:
        verbose_name = "Bất động sản"
        verbose_name_plural = "DS Bất động sản"
        indexes = (
            # Full text search index
            GinIndex(fields=["street", "address"]),
            # Search for code with like
            BTreeIndex(fields=['code']),
            # Search using IN query
            BTreeIndex(fields=['bedrooms', 'bathrooms', 'direction']),
            # Exact search
            models.Index(fields=["state", "district", "ward"]),
            models.Index(fields=["house_type", "transaction_type"]),
        )

    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name=_("Chuyên viên"))
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices,
                                        default=TransactionType.SELL, verbose_name=_("Hình thức giao dịch"))
    house_type = models.CharField(max_length=20, choices=HouseType.choices, default=HouseType.TOWN_HOUSE,
                                  verbose_name=_("Loại BĐS"))

    code = models.CharField(max_length=80, verbose_name=_("Mã BĐS (VIẾT HOA)"), help_text=_(
        "Quy tắc: Viết tắt chữ cái đầu Loại BĐS + 2 chữ số Năm + Tháng + Chữ cái đầu tên của Chuyên viên + Số BĐS của ĐC"),
                            unique=True)
    title = models.CharField(max_length=200, verbose_name=_("Tiêu đề đăng (VIẾT HOA)"),
                             help_text=_(
                                 "Gợi ý: Từ khoá + Vị trí (Đường/Phố/Khu) + Diện tích + Tiện ích + Giá + Sổ"))
    address = models.CharField(max_length=255, verbose_name=_("Địa chỉ đầy đủ"),
                               help_text=_("Ngõ.Ngách.Hẻm.Số nhà, Khu dân cư, Phố, Quận/Huyện, Tỉnh/TP"))
    urban_area = models.CharField(max_length=100, verbose_name=_("Khu đô thị/Khu dân cư"), blank=True,
                                  null=True)
    street = models.CharField(max_length=125, verbose_name=_("Tên đường, phố"),
                              default=_("Nhập tên Đường/Phố/Thôn/Xóm"), null=True)
    state = models.CharField(max_length=50, choices=city_choices, default="01",
                             verbose_name=_("Thành phố/Tỉnh"), )
    district = models.CharField(max_length=50, verbose_name=_("Quận/Huyện"), default="008")
    ward = models.CharField(max_length=50, verbose_name=_("Phường/Xã"), blank=True, null=True)

    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.OLD,
                                 verbose_name=_("Tình trạng BĐS"), null=True)
    year = models.CharField(max_length=50, verbose_name=_("Năm xây dựng/Còn lại"), blank=True, null=True,
                            help_text=_("Điền năm xây dựng/Tỷ lệ % sử dụng còn lại"))
    road_type = models.CharField(max_length=20, choices=RoadType.choices, default=RoadType.ALLEY_CAR,
                                 verbose_name=_("Đường/Ngõ trước nhà"))
    lane_width = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                     verbose_name=_("Chiều rộng đường/ngõ (m)"))
    area = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Diện tích (m2)"), default="30")
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Mặt tiền (m)"), default="4")
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Chiều dài (m)"), null=True,
                                 blank=True)
    area_real = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Diện tích thực tế(m2)"),
                                    null=True, blank=True)
    floors = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                 choices=([(i, i) for i in range(0, 20)]), verbose_name=_("Số tầng"))
    bedrooms = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(0, 20)]), verbose_name=_("Số phòng ngủ"),
                                   null=True)
    bathrooms = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    choices=([(i, i) for i in range(0, 20)]), verbose_name=_("Số phòng tắm"),
                                    null=True)
    direction = models.CharField(max_length=20, choices=Direction.choices, default=Direction.none,
                                 verbose_name=_("Hướng"))
    description = models.TextField(blank=True, verbose_name=_("Mô tả ngắn gọn"), help_text=_(
        "Mô tả giới thiệu BĐS ngắn gọn "))
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

    def __str__(self):
        self.title = "Bất động sản"
        return self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.address:
            state_name = get_state_name(self.state)
            district_name = get_ward_name(self.district)
            self.address = f"{self.street}, {district_name} {state_name}"
        super().save(*args, **kwargs)

    @property
    def main_photo(self):
        return self.listingimage_set.order_by('sort').first()

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
        if not self.ward:
            return ""
        return get_ward_name(self.district, self.ward)

    def district_name(self):
        return get_district_name(self.district)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "district": self.district,

        }

    registration_type = models.CharField(max_length=20, choices=RegistrationType.choices, blank=True,
                                         null=True, default=RegistrationType.RED_BOOK,
                                         verbose_name=_("Loại chứng nhận"))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá chào (tỷ)"))
    receive_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá thu về (tỷ)"),
                                        blank=True, null=True)
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá Hạ chào (tỷ)"),
                                     blank=True, null=True)
    bonus_rate = models.DecimalField(max_digits=2, decimal_places=1, verbose_name=_("Tỷ lệ trích thưởng (%)"),
                                     default="3")
    reward = models.DecimalField(max_digits=5, decimal_places=0,
                                 verbose_name=_("Số tiền trích thưởng (triệu)"), default="100", blank=True,
                                 null=True)

    reward_person = models.CharField(max_length=50, blank=True, verbose_name=_("Tên chủ sở hữu BĐS"),
                                     help_text="Tên người chủ sở hữu BĐS", default="Nguyễn Văn A")
    reward_person_mobile = models.CharField(max_length=50, blank=True, verbose_name=_("Số ĐT chủ sở hữu BĐS"),
                                            help_text="Số ĐT chủ sở hữu BĐS", default="0916286256")

    extra_data = models.TextField(max_length=250, verbose_name=_("Ghi chú"), null=True, blank=True,
                                  default="Chủ nhà hiểu chuyện, tôn trọng môi giới, thiện chí hợp tác,..",
                                  help_text="Ghi các thông tin khác quan trọng về chủ nhà, các yếu tố khác liên quan...")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SELLING,
                              verbose_name=_("Trạng thái giao dịch"))
    is_verified = models.BooleanField(default=False, verbose_name=_("ĐÃ XÁC MINH THÔNG TIN"))
    is_exclusive = models.BooleanField(default=False, verbose_name=_("THẾ GIỚI NHÀ PHỐ ĐỘC QUYỀN"))
    is_published = models.BooleanField(default=True, verbose_name=_("CHO PHÉP ĐĂNG"))
    list_date = models.DateTimeField(default=datetime.now, verbose_name=_("Ngày đăng"))

    location = LocationField(based_fields=['address'], zoom=7, null=True,
                             default=Point(105.8401439, 21.0334474), verbose_name=_("Toạ độ vị trí BĐS"),
                             help_text="Nhập toạ độ hoặc chọn vị trí trên bản đồ")


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


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        exclude = ('address',)

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
