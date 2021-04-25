from datetime import datetime

from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _
from location_field.models.spatial import LocationField
from embed_video.fields import EmbedVideoField
from FunctionModule.cadastral.constants import state_data, district_data
from FunctionModule.realtors.models import Realtor

class TransactionType(models.TextChoices):
    SELL = 'sell', _("Bán")
    FOR_RENT = 'for_rent', _("Cho thuê")
    PROJECT = 'project', _("Dự án")


class HouseType(models.TextChoices):
    STREET_HOUSE = 'street_house', _("Nhà mặt phố")
    CITY_HOUSE = 'city_house', _("Nhà phố")
    SHOP_HOUSE = 'shop_house', _("Cửa hàng")
    BUILDING = 'building', _("Toà nhà")
    OFFICE = 'office', _("Văn phòng")
    APARTMENT = 'apartment', _("Căn hộ")
    VILLA = 'villa', _("Biệt thự")
    LAND = 'land', _("Đất nền")



class RegistrationType(models.TextChoices):
    RED_BOOK = 'red_book', _("Sổ Đỏ")
    PINK_BOOK = 'pink_book', _("Sổ Hồng")
    DONT_BOOK = 'dont_book', _("Chưa làm sổ")


class RoadType(models.TextChoices):
    ALLEY_CAR = 'alley_car', _("Ngõ ô tô")
    ALLEY_BIKE = 'alley_bike', _("Ngõ xe máy")
    STREET_SURFACE = 'street_surface', _("Mặt tiền phố")


city_choices = [(k, v['name']) for k, v in state_data.items()]
city_choices.sort()


class Listing(models.Model):
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices, default=TransactionType.SELL,
                                  verbose_name=_("Hình thức giao dịch"))
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name=_("Đầu chủ"))
    state = models.CharField(max_length=50, choices=city_choices, default="01",
                             verbose_name=_("Thành phố/Tỉnh"), )
    district = models.CharField(max_length=50, verbose_name=_("Quận/Huyện"))
    ward = models.CharField(max_length=50, verbose_name=_("Phường/Xã"), blank=True)
    urban_area = models.CharField(max_length=100, verbose_name=_("Khu đô thị/Khu dân cư"), blank=True)
    street = models.CharField(max_length=125, verbose_name=_("Phố"), help_text=_("Tên đường, phố"), null = True)
    address = models.CharField(max_length=255, verbose_name=_("Địa chỉ đầy đủ"),  help_text=_("Số nhà/hẻm/ngách/ngõ"))
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
    house_type = models.CharField(max_length=20, choices=HouseType.choices, default=HouseType.CITY_HOUSE,
                                  verbose_name=_("Loại nhà"))
    road_type = models.CharField(max_length=20, choices=RoadType.choices, default=RoadType.STREET_SURFACE,
                                 verbose_name=_("Loại mặt tiền"))
    registration_type = models.CharField(max_length=20, choices=RegistrationType.choices,
                                         default=RegistrationType.RED_BOOK, verbose_name=_("Loại chứng nhận"))
    price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_("Giá chào (tỷ)"))
    sale_price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_("Giá Hạ chào (tỷ)"), blank=True, null=True)

    direction = models.CharField(choices=(('east', _("Đông")), ('east-south', _("Đông - Nam")), ('south', _("Nam")),  ('west-south', _("Tây - Nam")), ('west', _("Tây")), ('west-north', _("Tây - Bắc")),
                                          ('north', _("Bắc")), ('east-north', _("Đông - Bắc"))), default='east', max_length=12,
                                 verbose_name=_("Hướng"))
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                   choices=([(i, i) for i in range(1, 10)]),
                                   verbose_name=_("Số phòng ngủ"))
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, verbose_name=_("Diện tích phòng tắm"),
                                    blank=True, null=True)
    lane_width = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                     verbose_name=_("Rộng mặt đường/ngõ (m)"))
    lot_size = models.DecimalField(max_digits=5, decimal_places=1, default=0,
                                   verbose_name=_("Diện tích khuân viên"), )
    description = models.TextField(blank=True, verbose_name=_("Mô tả"), default="")
    location = LocationField(based_fields=['address'], zoom=7, null=True,
                             default=Point(105.8401439, 21.0334474))

    extra_data = models.JSONField(verbose_name=_("Thông tin khác"), null=True, blank=True, default=dict)
    list_date = models.DateTimeField(default=datetime.now, verbose_name=_("Ngày đăng"))
    title = models.CharField(max_length=200, verbose_name=_("Tên BĐS"),
                             help_text=_("[Tên phố - Quận/Huyện] [Diện tích - Tầng/Đất/CC - Mặt tiền] [Ngõ] [Giá]"))
    code = models.CharField(max_length=50, verbose_name=_("Mã BĐS"), help_text=_("Được điền tự động và duy nhất"),
                            unique=True)

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


def get_image_path(instance, filename: str):
    return 'photos/listings/' + str(instance.listing.id) + '/' + filename


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
