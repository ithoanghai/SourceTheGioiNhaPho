from django.db import models
from django.utils.translation import gettext as _

from FunctionModule.cadastral.constants import state_data

bedroom_choices = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10
}

price_choices = {
    '2000000000': '2 tỷ',
    '3000000000': '3 tỷ',
    '4000000000': '4 tỷ',
    '5000000000': '5 tỷ',
    '6000000000': '6 tỷ',
    '7000000000': '7 tỷ',
    '8000000000': '8 tỷ',
    '9000000000': '9 tỷ',
    '10000000000': '10 tỷ',
    '20000000000': '20 tỷ',
}
city_choices = [(k, v['name']) for k, v in state_data.items()]
city_choices.sort()


class TransactionType(models.TextChoices):
    SELL = 'sell', _("Bán")
    FOR_RENT = 'for_rent', _("Cho thuê")
    PROJECT = 'project', _("Dự án")


class HouseType(models.TextChoices):
    STREET_HOUSE = 'street_house', _("Nhà mặt phố")
    TOWN_HOUSE = 'town_house', _("Nhà phố")
    LOFT_HOUSE = 'loft_house', _("Nhà gác xép/Cấp 4")
    SHOP_HOUSE = 'shop_house', _("Cửa hàng")

    BUILDING = 'building', _("Toà nhà")
    BUILDING_BUSINESS = 'building_business', _("Toà nhà kinh doanh")
    OFFICE = 'office', _("Văn phòng")
    OFFICE_TEL = 'office_tel', _("Văn phòng khách sạn")
    CONDO_TEL = 'condo_tel', _('Căn hộ khách sạn')
    APARTMENT = 'apartment', _("Căn hộ")
    SERVICE_APARTMENT = 'service_apartment', _("Căn hộ dịch vụ")
    PENT_HOUSE = 'pent_house', _("Căn hộ áp mái")
    VILLA = 'villa', _("Biệt thự")
    VILLA_REST = 'villa_rest', _("Biệt thự nghỉ dưỡng")
    LAND = 'land', _("Đất nền")
    LAND_BUSINESS = 'land_business', _("Mặt bằng kinh doanh")
    PLOT = 'plot', _("Đất phân lô")
    INDUSTRIAL_LAND = 'industrial_land', _("Đất công nghiệp")
    WAREHOUSE_WORKSHOP = 'warehouse_workshop', _("Kho xưởng")
    OTHER = 'other', _("Khác")


class RegistrationType(models.TextChoices):
    RED_BOOK = 'red_book', _("Sổ Đỏ")
    PINK_BOOK = 'pink_book', _("Sổ Hồng")
    DONT_BOOK = 'dont_book', _("Chưa làm sổ")


class RoadType(models.TextChoices):
    ALLEY_CAR = 'alley_car', _("Ngõ ô tô")
    ALLEY_BIKE = 'alley_bike', _("Ngõ xe máy")
    ALLEY_TRIBIKE = 'alley_tribike', _("Ngõ Ba gác")
    STREET_SURFACE = 'street_surface', _("Mặt tiền phố")


class Status(models.TextChoices):
    NEW = 'new', _("Mới")
    SELLING = 'selling', _("Còn bán")
    STOP_SELLING = 'stop_selling', _("Dừng bán")
    SOLD = 'sold', _("Đã bán")
    SALE = 'sale', _("Hạ chào")
