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
                      RoadType, Status, Direction, Condition)


def get_image_path(instance, filename: str):
    return 'photos/listings/' + str(instance.listing.id) + '/' + filename


class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name=_("Đầu chủ"))
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices,
                                        default=TransactionType.SELL,verbose_name=_("Hình thức giao dịch"))
    code = models.CharField(max_length=80, verbose_name=_("Mã BĐS"), help_text=_(
        "Quy tắc: Viết tắt chữ cái đầu Loại BĐS + 2 chữ số Năm + Tháng + Chữ cái đầu tên Đầu chủ + Số BĐS của ĐC"),unique=True)
    title = models.CharField(max_length=200, verbose_name=_("Tiêu đề đăng"),
                             help_text=_( "Gợi ý: Từ khoá + Vị trí (Đường/Phố/Khu) + Diện tích + Tiện ích + Giá + Sổ"))
    address = models.CharField(max_length=255, verbose_name=_("Địa chỉ ngắn gọn"), help_text=_("Ngõ.Ngách.Hẻm.Số nhà"))
    urban_area = models.CharField(max_length=100, verbose_name=_("Khu đô thị/Khu dân cư"), blank=True, null=True)
    street = models.CharField(max_length=125, verbose_name=_("Tên đường, phố"), default=_("Nhập tên Đường/Phố/Thôn/Xóm"), null=True)
    state = models.CharField(max_length=50, choices=city_choices, default="01",
                             verbose_name=_("Thành phố/Tỉnh"), )
    district = models.CharField(max_length=50, verbose_name=_("Quận/Huyện"))
    ward = models.CharField(max_length=50, verbose_name=_("Phường/Xã"), blank=True, null=True)

    house_type = models.CharField(max_length=20, choices=HouseType.choices, default=HouseType.TOWN_HOUSE,verbose_name=_("Loại nhà"))
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.OLD,verbose_name=_("Tình trạng BĐS"), null=True)
    year = models.CharField(max_length=50, verbose_name=_("Năm xây dựng/Còn lại"), help_text=_("Điền năm xây dựng/Tỷ lệ % sử dụng còn lại"))
    road_type = models.CharField(max_length=20, choices=RoadType.choices, default=RoadType.ALLEY_CAR,
                                 verbose_name=_("Đường/Ngõ trước nhà"))
    lane_width = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Chiều ộng đường/ngõ (m)"))
    area = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Diện tích (m2)"))
    width = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Mặt tiền (m)"))
    length = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Chiều dài (m)"), null=True, blank=True)
    area_real = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Diện tích thực tế(m2)"))
    floors = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                 choices=([(i, i) for i in range(0, 20)]), verbose_name=_("Số tầng"))
    bedrooms = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(0, 20)]), verbose_name=_("Số phòng ngủ"), null=True)
    bathrooms = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(0, 20)]), verbose_name=_("Số phòng tắm"), null=True)
    direction = models.CharField(max_length=20, choices=Direction.choices, default=Direction.none,verbose_name=_("Hướng"))
    description = models.TextField(blank=True, verbose_name=_("Mô tả"), default=_("Vị trí cực đẹp, thuận tiện đi lại, chỉ phút mốt ra trung tâm, đường chính, hồ, bến tàu, xe,..Thiết kế hiện đại, đầy đủ công năng, khung cột bê tông chắc chắn.., các phòng, khuôn viên rộng rãi, hướng đẹp, mát,.. Tiện ích tràn ngập như BĐS có bể bơi, phòng xông hơi, phòng xem phim, giải trí, thể thao, chỗ đỗ xe hơi... Gần rạp chiếu phim, TTTM, bể bơi, khu vui chơi, thể thao,...An sinh khu vực đỉnh gần bệnh viện, trường học, khu dân trí cao, an ninh tốt,...Pháp lý đầy đủ, sổ đẹp vuông cất két…"))

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

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "district": self.district,

        }

    location = LocationField(based_fields=['address'], zoom=7, null=True,default=Point(105.8401439, 21.0334474))

    registration_type = models.CharField(max_length=20, choices=RegistrationType.choices, blank=True,
                                         null=True, default=RegistrationType.RED_BOOK, verbose_name=_("Loại chứng nhận"))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá chào (tỷ)"))
    receive_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá thu về (tỷ)"))
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Giá Hạ chào (tỷ)"),blank=True, null=True)
    bonus_rate = models.DecimalField(max_digits=2, decimal_places=1, verbose_name=_("Tỷ lệ trích thưởng (%)"))
    reward = models.DecimalField(max_digits=5, decimal_places=0, verbose_name=_("Số tiền trích thưởng (triệu)"))

    reward_person = models.TextField(blank=True, verbose_name=_("Tên chủ sở hữu BĐS"), help_text="Tên người chủ sở hữu BĐS")
    reward_person_mobile = models.TextField(blank=True, verbose_name=_("Số ĐT chủ sở hữu BĐS"),help_text="Số ĐT chủ sở hữu BĐS")

    extra_data = models.TextField(verbose_name=_("Ghi chú"), null=True, blank=True, default="Chủ nhà hiểu chuyện, tôn trọng môi giới, thiện chí hợp tác,..",help_text="Ghi các thông tin khác quan trọng về chủ nhà, các yếu tố khác liên quan...")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SELLING, verbose_name=_("Trạng thái giao dịch"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Đã xác minh thông tin nhà"))
    is_exclusive = models.BooleanField(default=False, verbose_name=_("Nhà Phố độc quyền"))
    is_published = models.BooleanField(default=True, verbose_name=_("Được phép đăng"))
    list_date = models.DateTimeField(default=datetime.now, verbose_name=_("Ngày đăng"))

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

class ContractImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    sort = models.IntegerField(default=0, verbose_name=_("Thứ tự hiện"))
    description = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Thông tin"))
    photo = models.ImageField(upload_to=get_image_path, blank=False, verbose_name=_("Ảnh"))

    def __str__(self):
        return f'{self.listing_id}_{self.sort}__{self.photo.url}'

    @property
    def url(self):
        return self.photo.url