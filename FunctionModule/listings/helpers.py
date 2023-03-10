import sys
import traceback

from FunctionModule.listings.choices import HouseType, RoadType, Status, TransactionType, Direction, RegistrationType


def get_house_type_short(house_type: str) -> str:
    if house_type == HouseType.STREET_HOUSE:
        return 'SH'
    elif house_type == HouseType.TOWN_HOUSE:
        return 'NG'
    elif house_type == HouseType.VILLA or house_type == HouseType.VILLA_REST:
        return 'BT'
    elif house_type == HouseType.PLOT:
        return 'LK'
    elif house_type == HouseType.LOFT_HOUSE:
        return 'C4'
    elif house_type == HouseType.LAND:
        return 'DN'
    elif house_type == HouseType.SHOP_HOUSE:
        return 'CH'
    elif house_type == HouseType.APARTMENT or house_type == HouseType.CONDO_TEL or house_type == HouseType.SERVICE_APARTMENT or house_type == HouseType.PENT_HOUSE:
        return 'CC'
    elif house_type == HouseType.BUILDING or house_type == HouseType.BUILDING_BUSINESS:
        return 'BD'
    elif house_type == HouseType.OFFICE or house_type == HouseType.OFFICE_TEL:
        return 'OF'
    elif house_type == HouseType.WAREHOUSE_WORKSHOP:
        return 'WF'
    else:
        return 'NP'


def get_short_title_from_transaction_type(transaction_type: str):
    if transaction_type == TransactionType.SELL:
        return 'Bán'
    elif transaction_type == TransactionType.FOR_RENT:
        return 'Cho thuê'
    elif transaction_type == TransactionType.PROJECT:
        return 'Dự án'


def get_short_title_from_house_type(house_type: str):
    if house_type == HouseType.VILLA:
        return 'Biệt thự'
    elif house_type == HouseType.VILLA_REST:
        return 'Biệt thự nghỉ dưỡng'
    elif house_type == HouseType.STREET_HOUSE:
        return 'Nhà mặt phố'
    elif house_type == HouseType.TOWN_HOUSE or house_type == HouseType.LOFT_HOUSE:
        return 'Nhà phố'
    elif house_type == HouseType.LAND or house_type == HouseType.INDUSTRIAL_LAND:
        return 'Đất'
    elif house_type == HouseType.PLOT:
        return 'Đất phân lô'
    elif house_type == HouseType.LAND_BUSINESS:
        return 'Mặt bằng kinh doanh'
    elif house_type == HouseType.WAREHOUSE_WORKSHOP:
        return 'Kho xưởng'
    elif house_type == HouseType.SHOP_HOUSE:
        return 'Cửa hàng'
    elif house_type == HouseType.APARTMENT or house_type == HouseType.PENT_HOUSE:
        return 'Căn hộ'
    elif house_type == HouseType.CONDO_TEL or house_type == HouseType.SERVICE_APARTMENT:
        return 'Căn hộ nghỉ dưỡng'
    elif house_type == HouseType.OFFICE or house_type == HouseType.OFFICE_TEL:
        return 'Văn phòng'
    elif house_type == HouseType.BUILDING or house_type == HouseType.BUILDING_BUSINESS:
        return 'Tòa nhà'
    else:
        return 'Nhà trong ngõ'


def get_short_title_from_road_type(road_type: str):
    if road_type == RoadType.ALLEY_CAR_2:
        return 'Ô tô tránh'
    elif road_type == RoadType.ALLEY_CAR_TRIBIKE:
        return 'Ô tô tránh Ba gác'
    elif road_type == RoadType.ALLEY_CAR:
        return 'Chỉ 1 Ô tô'
    elif road_type == RoadType.ALLEY_TRIBIKE_BIKE:
        return 'Ba gác tránh Xe máy'
    elif road_type == RoadType.ALLEY_TRIBIKE:
        return 'Chỉ 1 Ba gác'
    elif road_type == RoadType.ALLEY_BIKE:
        return 'Xe máy tránh nhau'


def get_listing_status_title_from_code(listing_status: str):
    if listing_status == Status.SELLING:
        return 'ĐANG'
    elif listing_status == Status.SOLD:
        return 'ĐÃ'
    elif listing_status == Status.STOP_SELLING:
        return 'DỪNG'
    elif listing_status == Status.SALE:
        return 'HẠ GIÁ'


def get_short_title_from_direction(direction: str):
    if direction == Direction.east:
        return 'Đông'
    elif direction == Direction.south_east:
        return 'Đông - Nam'
    elif direction == Direction.south:
        return 'Nam'
    elif direction == Direction.south_west:
        return 'Tây - Nam'
    elif direction == Direction.west:
        return 'Tây'
    elif direction == Direction.north_west:
        return 'Tây - Bắc'
    elif direction == Direction.north:
        return 'Bắc'
    elif direction == HouseType.north_east:
        return 'Đông - Bắc'


def get_short_title_from_registration_type(registration_type: str):
    if registration_type == RegistrationType.RED_PINK_BOOK:
        return 'Sổ Đỏ/ Sổ hồng'
    elif registration_type == RegistrationType.VALID_DOCUMENTS:
        return 'Giấy tờ hợp lệ'
    elif registration_type == RegistrationType.CONSTRUCTION_LICENSE:
        return 'Giấy phép xây dựng'
    elif registration_type == RegistrationType.BUSINESS_LICENSE:
        return 'Giấy phép kinh doanh'
    elif registration_type == RegistrationType.PREPARE_BOOK:
        return 'Chuẩn bị làm sổ'
    elif registration_type == RegistrationType.DONT_BOOK:
        return 'Chưa có sổ'
    elif registration_type == RegistrationType.OTHER:
        return 'Khác'


def print_trace(e: Exception):
    trace = traceback.extract_tb(sys.exc_info()[2])
    # Add the event to the log
    output = "Error in the server: %s.\n" % (e)
    output += "\tTraceback is:\n"
    for (file, linenumber, affected, line) in trace:
        output += "\t> Error at function %s\n" % (affected)
        output += "\t  At: %s:%s\n" % (file, linenumber)
        output += "\t  Source: %s\n" % (line)
    output += "\t> Exception: %s\n" % (e)
    print(output)


def get_menu_from_choices():
    listChoices = []

    return HouseType.choices