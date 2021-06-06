from __future__ import unicode_literals

from datetime import datetime

from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _
from embed_video.fields import EmbedVideoField
from location_field.models.spatial import LocationField
from rest_framework import serializers

from FunctionModule.cadastral.constants import state_data, district_data
from FunctionModule.realtors.models import Realtor
from .choices import (TransactionType, city_choices, HouseType, RegistrationType,
                      RoadType, Status)


def get_image_path(instance, filename: str):
    return 'photos/listings/' + str(instance.listing.id) + '/' + filename


class Listing(models.Model):
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices,
                                        default=TransactionType.SELL,
                                        verbose_name=_("Hình thức giao dịch"))
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name=_("Đầu chủ"))
    state = models.CharField(max_length=50, choices=city_choices, default="01",
                             verbose_name=_("Thành phố/Tỉnh"), )
    district = models.CharField(max_length=50, verbose_name=_("Quận/Huyện"))
    ward = models.CharField(max_length=50, verbose_name=_("Phường/Xã"), blank=True, null=True)
    urban_area = models.CharField(max_length=100, verbose_name=_("Khu đô thị/Khu dân cư"), blank=True,
                                  null=True)
    street = models.CharField(max_length=125, verbose_name=_("Phố"), help_text=_("Tên đường, phố"), null=True)
    address = models.CharField(max_length=255, verbose_name=_("Địa chỉ đầy đủ"),
                               help_text=_("Số nhà/hẻm/ngách/ngõ"))
    area = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Diện tích"))
    area_unit = models.CharField(max_length=5, default='m2', verbose_name=_("Đơn vị diện tích"),
                                 choices=[('m2', 'm2')])
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Chiều dài"), null=True,
                                 blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Chiều rộng"), blank=True,
                                null=True)
    floors = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                 choices=([(i, i) for i in range(1, 10)]),
                                 verbose_name=_("Số tầng"))
    house_type = models.CharField(max_length=20, choices=HouseType.choices, default=HouseType.TOWN_HOUSE,
                                  verbose_name=_("Loại nhà"))
    road_type = models.CharField(max_length=20, choices=RoadType.choices, default=RoadType.STREET_SURFACE,
                                 verbose_name=_("Loại mặt tiền"))
    registration_type = models.CharField(max_length=20, choices=RegistrationType.choices, blank=True,
                                         null=True, default=RegistrationType.RED_BOOK,
                                         verbose_name=_("Loại chứng nhận"))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá chào (tỷ)"))
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá Hạ chào (tỷ)"),
                                     blank=True, null=True)

    direction = models.CharField(choices=(
        ('east', _("Đông")), ('south-east', _("Đông - Nam")), ('south', _("Nam")),
        ('south-west', _("Tây - Nam")),
        ('west', _("Tây")), ('north-west', _("Tây - Bắc")),
        ('north', _("Bắc")), ('north-east', _("Đông - Bắc"))), default='east', max_length=12,
        verbose_name=_("Hướng"))
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(1, 10)]),
                                   verbose_name=_("Số phòng ngủ"), null=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, verbose_name=_("Diện tích phòng tắm"),
                                    blank=True, null=True)
    lane_width = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                     verbose_name=_("Rộng mặt đường/ngõ (m)"))
    lot_size = models.DecimalField(max_digits=5, decimal_places=1, default=0,
                                   verbose_name=_("Diện tích khuôn viên"), null=True, blank=True)
    description = models.TextField(blank=True, verbose_name=_("Mô tả"), default="")
    location = LocationField(based_fields=['address'], zoom=7, null=True,
                             default=Point(105.8401439, 21.0334474))

    extra_data = models.JSONField(verbose_name=_("Thông tin khác"), null=True, blank=True, default=dict)
    list_date = models.DateTimeField(default=datetime.now, verbose_name=_("Ngày đăng"))
    title = models.CharField(max_length=200, verbose_name=_("Tên BĐS"),
                             help_text=_(
                                 "[Tên phố - Quận/Huyện] [Diện tích - Tầng/Đất/CC - Mặt tiền] [Ngõ] [Giá]"))
    code = models.CharField(max_length=80, verbose_name=_("Mã BĐS"),
                            help_text=_("Được điền tự động và duy nhất"),
                            unique=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SELLING,
                              verbose_name=_("Tình trạng BĐS"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Đã xác minh thông tin nhà"))
    is_exclusive = models.BooleanField(default=False, verbose_name=_("Nhà Phố độc quyền"))
    is_published = models.BooleanField(default=True, verbose_name=_("Được phép đăng"))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.address:
            state_name = state_data[self.state]['name']
            district_name = next(x['name'] for x in district_data[self.state] if x['code'] == self.district)
            self.address = f"{self.street}, {district_name} {state_name}"
        super().save(*args, **kwargs)

    @property
    def main_photo(self):
        return self.listingimage_set.order_by('sort').first()

    @property
    def photos(self):
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

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "district": self.district,

        }


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    sort = models.IntegerField(default=0, verbose_name=_("Thứ tự hiện"))
    description = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Thông tin"))
    photo = models.ImageField(upload_to=get_image_path, blank=False, verbose_name=_("Ảnh"))

    def __str__(self):
        return f'{self.listing_id}_{self.sort}__{self.photo.url}'

    @property
    def url(self):
        return self.photo.url


class ListingVideo(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    video = EmbedVideoField()


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        # fields = '__all__'
        exclude = ('address',)

    lat = serializers.CharField()
    long = serializers.CharField()
    main_photo = serializers.SerializerMethodField()

    def get_main_photo(self, obj):
        photo = obj.main_photo
        if photo:
            return photo.url
        else:
            return ''
