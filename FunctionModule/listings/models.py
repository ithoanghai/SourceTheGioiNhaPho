from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from FunctionModule.realtors.models import Realtor


class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name=_("Đầu chủ"))
    title = models.CharField(max_length=200, verbose_name=_("Tên nhà"))
    address = models.CharField(max_length=200, verbose_name=_("Địa chỉ"))
    city = models.CharField(max_length=100, verbose_name=_("Thành phố"))
    state = models.CharField(max_length=100, verbose_name=_("Huyện"))
    description = models.TextField(blank=True, verbose_name=_("Mô tả"))
    price = models.IntegerField(verbose_name=_("Giá chào"))
    bedrooms = models.IntegerField(verbose_name=_("Số phòng ngủ"))
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1, verbose_name=_("Diện tích phòng tắm"))
    garage = models.BooleanField(default=0, verbose_name=_("Có nơi để ô tô"))
    area = models.DecimalField(verbose_name=_("Diện tích (m2)"), max_digits=5, decimal_places=1)
    lot_size = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Diện tích vườn (m2)"))
    is_published = models.BooleanField(default=True, verbose_name=_("Được phép đăng"))
    list_date = models.DateTimeField(default=datetime.now, blank=True, verbose_name=_("Ngày đăng"))

    def __str__(self):
        return self.title

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
