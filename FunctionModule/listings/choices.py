from django.db import models
from django.utils.translation import gettext_lazy as _

from FunctionModule.cadastral.constants import state_data, ward_data, all_districts, district_data, all_wards

city_choices = [(k, v['name']) for k, v in state_data.items()]
city_choices.sort()
district_choices = [(k, v['name']) for k, v in all_districts.items()]
district_choices.sort()
district_default_choices = [(d['code'], d['name']) for d in district_data['01']]
ward_default_choices = [(d['code'], d['name']) for d in ward_data['008']]

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
    '1000000000': '1 tỷ',
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


class TransactionType(models.TextChoices):
    SELL = 'sell', _("Bán")
    FOR_RENT = 'rent', _("Cho thuê")
    PROJECT = 'project', _("Dự án")


# House type in facebook
# "apartment", "apartment_room", "builder_floor", "bungalow", "condo", "condo_room", "house", "house_in_condominium", \
# "house_in_villa", "house_room", "land", "loft", "manufactured", "other", "other_room", "penthouse", "single_family_home", \
# "studio", "townhouse", "townhouse_room"
class HouseType(models.TextChoices):
    STREET_HOUSE = 'street_house', _("Nhà mặt phố")
    TOWN_HOUSE = 'town_house', _("Nhà phố")
    LOFT_HOUSE = 'loft_house', _("Nhà 1 tầng/Cấp 4")
    SHOP_HOUSE = 'shop_house', _("Cửa hàng/ShopHouse")
    APARTMENT = 'apartment', _("Căn hộ/Chung cư MN/Nhà tập thể")
    VILLA = 'villa', _("Biệt thự")
    PLOT = 'plot', _("Liền kề/Phân lô/Dịch vụ")
    LAND = 'land', _("Đất nền")
    BUILDING = 'building', _("Toà nhà")
    BUILDING_BUSINESS = 'building_business', _("Toà nhà kinh doanh")
    OFFICE = 'office', _("Văn phòng")
    OFFICE_TEL = 'office_tel', _("Văn phòng khách sạn")
    CONDO_TEL = 'condo_tel', _('Căn hộ khách sạn')
    SERVICE_APARTMENT = 'service_apartment', _("Căn hộ dịch vụ")
    PENT_HOUSE = 'pent_house', _("Căn hộ áp mái")
    VILLA_REST = 'villa_rest', _("Biệt thự nghỉ dưỡng")
    LAND_BUSINESS = 'land_business', _("Mặt bằng kinh doanh")
    INDUSTRIAL_LAND = 'industrial_land', _("Đất công nghiệp")
    WAREHOUSE_WORKSHOP = 'warehouse_workshop', _("Kho xưởng")
    OTHER = 'other', _("Khác")


class FurnishType(models.TextChoices):
    FURNISHED = 'furnished', _("Đủ đồ đạc")
    SEMI_FURNISHED = 'semi_furnished', _("Một số đồ đạc")
    UNFURNISHED = 'unfurnished', _("Không có đồ đạc")


class RegistrationType(models.TextChoices):
    RED_PINK_BOOK = 'red_pink_book', _("Sổ Đỏ/ Sổ hồng")
    VALID_DOCUMENTS = 'valid_documents', _("Giấy tờ hợp lệ")
    CONSTRUCTION_LICENSE = 'construction_license', _("Giấy phép xây dựng")
    BUSINESS_LICENSE = 'business_license', _("Giấy phép kinh doanh")
    PREPARE_BOOK = 'prepare_book', _("Chuẩn bị làm sổ")
    DONT_BOOK = 'dont_book', _("Chưa có sổ")
    OTHER = 'other', _("Khác")


class RoadType(models.TextChoices):
    ALLEY_CAR_2 = 'alley_car_2', _("Ô tô tránh")
    ALLEY_CAR_TRIBIKE = 'alley_car_tribike', _("Ô tô tránh Ba gác")
    ALLEY_CAR = 'alley_car', _("Ô tô")
    ALLEY_TRIBIKE = 'alley_tribike', _("Ngõ Ba gác")
    ALLEY_TRIBIKE_BIKE = 'alley_tribike_bike', _("Ngõ Ba gác tránh Xe máy")
    ALLEY_BIKE = 'alley_bike', _("Ngõ Xe máy tránh nhau")


class ParkingType(models.TextChoices):
    GARAGE = 'garage', _("Có gara ô tô")
    OFF_STREET = 'off_street', _("Đỗ trước nhà")
    STREET = 'street', _("Đỗ ngoài đường")
    NONE = 'none', _("Không có chỗ đỗ")
    OTHER = 'other', _("Khác")


class Condition(models.TextChoices):
    NEW = 'new', _("Xây mới")
    OLD = 'old', _("Nhà cũ")
    RAW = 'raw', _("Xây thô")
    LAND = 'land', _("Đất nền")
    OTHER = 'other', _("Khác")


class Construction(models.TextChoices):
    RELEASE = 'release', _("Đã hoàn thiện")
    UNDER_CONSTRUCTION = 'under_construction', _("Đang thi công")
    PRERELEASE = 'pre_release', _("Sắp thi công")
    OTHER = 'other', _("Khác")


class Status(models.TextChoices):
    SELLING = 'selling', _("Còn bán")
    SALE = 'sale', _("Hạ chào")
    SOLD = 'sold', _("Đã bán")
    STOP_SELLING = 'stop_selling', _("Dừng bán")


class Direction(models.TextChoices):
    east = 'east', _("Đông")
    south_east = 'south-east', _("Đông - Nam")
    south = 'south', _("Nam")
    south_west = 'south-west', _("Tây - Nam")
    west = 'west', _("Tây")
    north_west = 'north-west', _("Tây - Bắc")
    north = 'north', _("Bắc")
    north_east = 'north-east', _("Đông - Bắc")


class Exhaustive(models.TextChoices):
    NOT = 'not', _("Chưa khảo sát")
    PREPARE = 'prepare', _("Lên lịch chuẩn bị khảo sát")
    INVESTIGATED = 'investigated', _("Đã khảo sát")


class LiquidClass(models.TextChoices):
    SUPER = 'super', _("A+_Cực dễ bán")
    EASY = 'easy', _("A_Dễ bán")
    NORMAL = 'normal', _("B_Bình thường")
    HARD = 'hard', _("C_Khó bán")
    VERY_HARD = 'very_hard', _("C_Rất khó bán")
    NOT_RATE = 'not_rate', _("Chưa đánh giá")
