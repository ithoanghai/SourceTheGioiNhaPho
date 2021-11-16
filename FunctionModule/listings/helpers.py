import sys
import traceback

from FunctionModule.listings.choices import HouseType


def get_house_type_short(house_type: str) -> str:
    if house_type == HouseType.STREET_HOUSE:
        return 'NP'
    elif house_type == HouseType.TOWN_HOUSE:
        return 'NG'
    elif house_type == HouseType.VILLA:
        return 'BT'
    elif house_type == HouseType.LOFT_HOUSE:
        return 'C4'
    elif house_type == HouseType.LAND:
        return 'DN'
    elif house_type == HouseType.SHOP_HOUSE:
        return 'CH'
    elif house_type == HouseType.APARTMENT:
        return 'CC'
    else:
        return 'NP'


def get_short_title_from_house_type(house_type: str):
    if house_type == HouseType.VILLA:
        return 'Biệt thự'
    elif house_type == HouseType.VILLA_REST:
        return 'Biệt thự nghỉ dưỡng'
    elif house_type == HouseType.LAND or HouseType.INDUSTRIAL_LAND:
        return 'Đất'
    elif HouseType.PLOT:
        return 'Đất phân lô'
    elif HouseType.LAND_BUSINESS:
        return 'Mặt bằng kinh doanh'
    elif HouseType.WAREHOUSE_WORKSHOP:
        return 'Kho xưởng'
    elif house_type == HouseType.SHOP_HOUSE:
        return 'Cửa hàng'
    elif house_type == HouseType.APARTMENT or house_type.PENT_HOUSE:
        return 'Căn hộ'
    elif house_type == HouseType.CONDO_TEL or HouseType.ERVICE_APARTMENT:
        return 'Căn hộ nghỉ dưỡng'
    elif house_type == HouseType.OFFICE or HouseType.OFFICE_TEL:
        return 'Văn phòng'
    elif house_type == HouseType.BUILDING or HouseType.BUILDING_BUSINESS:
        return 'Tòa nhà'
    elif house_type == HouseType.STREET_HOUSE:
        return 'Nhà mặt phố'
    elif house_type == HouseType.TOWN_HOUSE or HouseType.LOFT_HOUSE:
        return 'Nhà trong ngõ'
    else:
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
