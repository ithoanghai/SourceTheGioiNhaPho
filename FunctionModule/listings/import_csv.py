import csv
import datetime
import sys
import traceback
from decimal import Decimal

import pytz
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db.backends.utils import format_number
from django.utils.text import slugify
from geopy import GeocodeEarth
import logging
from FunctionModule.accounts.models import User
from FunctionModule.cadastral.constants import district_data
from FunctionModule.listings.models import Listing, Status, TransactionType, HouseType, RoadType
from FunctionModule.realtors.models import Realtor

default_password = 'tgnpvn@2021'
logger = logging.getLogger(__name__)

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


def read_header(header_row):
    header_dict = {
        "tgian": 0,
        "hien-trang": 1,
        "dia-chi": 2,
        "pho": 3,
        "quan": 4,
        "thong-so": 5,
        "gia": 6,
        "dau-chu": 7,
        "sdt": 8,
        "dac-diem": 10,
        "huong": 11,
        "dt": 14,
        "trm2": 15,
    }
    for index, field in enumerate(header_row):
        field = field.replace('Đ', 'd')
        field = slugify(field)
        if field in header_dict:
            if field == 'pho' and index > 3:
                continue
            header_dict[field] = index
    return header_dict


def get_direction(direction: str) -> str:
    code = ''
    if direction == 'Đông':
        code = 'east'
    elif direction == 'Tây':
        code = 'west'
    elif direction == 'Nam':
        code = 'south'
    elif direction == 'Bắc':
        code = 'north'
    elif direction == 'Đông Nam':
        code = 'south-east'
    elif direction == 'Đông Bắc':
        code = 'north-east'
    elif direction == 'Tây Nam':
        code = 'south-west'
    elif direction == 'Tây Bắc':
        code = 'north-west'

    return code


def handle_import(file_path):
    line_count = 0
    try:
        realtors = Realtor.objects.all()
        user_dict = {}
        for obj in realtors:
            user_dict[obj.user.phone] = obj

        listing_count = Listing.objects.count()
        limit = 1000
        listing_obj = {}
        api_key = getattr(settings, 'GEOEARTH_API_KEY', '')
        if listing_count > limit:
            cur = 0
            while cur < listing_count:
                listings = Listing.objects.all()[cur:limit + cur]
                for item in listings:  # type: Listing
                    listing_obj[item.code] = item
                cur = limit + cur
        else:
            listings = Listing.objects.all()
            for item in listings:  # type: Listing
                listing_obj[item.code] = item

        with open(file_path, 'w', encoding="utf-8", errors='ignore') as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            new_listings = []
            updated_listings = []
            hanoi_district_list = district_data["01"]
            hanoi_districts = {}
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')

            for item in hanoi_district_list:  # type: dict
                hanoi_districts[item['name']] = item['code']
            for row in csv_reader:
                line_count += 1

                if line_count == 11:
                    header_dict = read_header(row)
                if line_count > 11 and row[3]:
                    district = row[header_dict['quan']]
                    if not district:
                        logger.info(f"No district. Continue in line {line_count}")
                        continue
                    if district in hanoi_districts:
                        district_code = hanoi_districts[district]
                    else:
                        logger.info(f"District code not found. Continue in line {line_count}")
                        continue
                    try:
                        created = datetime.datetime.strptime(row[header_dict['tgian']], '%d/%m/%Y %H:%M:%S')
                        created = created.replace(tzinfo=timezone)
                    except ValueError:
                        created = datetime.datetime.now(tz=timezone)

                    status = row[header_dict['hien-trang']]
                    if not status:
                        status = Status.SELLING
                    else:
                        if status == 'Hạ chào':
                            status = Status.SALE
                        elif status == 'Còn bán':
                            status = Status.SELLING
                        elif status == 'Đã bán':
                            status = Status.SOLD
                        else:
                            status = Status.STOP_SELLING

                    addr = row[header_dict['dia-chi']].replace('.', '/')
                    street = row[header_dict['pho']]
                    # Hanoi
                    state = '01'
                    code = f"{district}-{street}-{addr}".lower().replace('đ', 'd').replace('õ', 'o')[:80]
                    code = slugify(code)
                    if code in listing_obj:
                        continue
                    encoded_num = row[header_dict['thong-so']]
                    # billion vnd
                    price = row[header_dict['gia']]
                    if not price:
                        continue
                    if price == '#VALUE!':
                        continue
                    price = Decimal(price)
                    # print("Price: ", price, format_number(price, 4, 2))
                    name = row[header_dict['dau-chu']]

                    phone = row[header_dict['sdt']]
                    phone = phone.split(' ')[0]
                    if not phone.isalnum():
                        logger.info(f"Phone invalid. Continue in line {line_count}")
                        continue
                    desc = row[header_dict['dac-diem']]
                    trans_type = TransactionType.SELL
                    house_type = HouseType.TOWN_HOUSE
                    road_type = RoadType.ALLEY_CAR_2

                    if desc == 'Đất Dự Án':
                        trans_type = TransactionType.PROJECT
                    elif desc == 'Kinh Doanh':
                        house_type = HouseType.SHOP_HOUSE
                    elif desc == 'Mặt Phố':
                        house_type = HouseType.STREET_HOUSE
                    elif desc == 'Ngõ Ô Tô':
                        road_type = RoadType.ALLEY_CAR
                    elif desc == 'Ngõ 3 Gác':
                        road_type = RoadType.ALLEY_TRIBIKE
                    elif desc == 'Ngõ Xe Máy':
                        road_type = RoadType.ALLEY_BIKE

                    splitter = encoded_num.split(' ')
                    splitter_len = len(splitter)
                    if splitter_len < 3:
                        logger.info(f"Cannot decode encoded_num. Continue in line {line_count}")
                        continue
                    # splitter = list(filter(None, splitter))
                    floor_area = splitter[0].split('/')
                    if splitter_len == 2:
                        lane_width = float(splitter[1].replace(',', '.'))
                    else:
                        try:
                            lane_width = float(splitter[2].replace(',', '.'))
                        except ValueError:
                            logger.info(f"Cannot decode floor_area. Continue in line {line_count}")
                            continue

                    floor_code = slugify(splitter[1].lower().replace('đ', 'd').replace('t', ''))
                    if floor_code == 'c4' or floor_code == 'c' or floor_code == 'cap 4':
                        floor = 1.0
                    elif floor_code == 'da' or floor_code == 'd':
                        floor = 1.0
                        house_type = HouseType.LAND
                    else:
                        if splitter_len == 2:
                            floor = float(len(floor_area))
                        else:
                            try:
                                floor = float(floor_code)
                            except ValueError:
                                logger.info(f"Cannot decode floor_code. Continue in line {line_count}")
                                continue
                    if not floor.is_integer():
                        continue
                    direction = get_direction(row[header_dict['huong']])
                    try:
                        #area = float(row[header_dict['dt']].replace('c4', ''))
                        area = float(row[header_dict['dt']])
                    except ValueError:
                        #logger.info(f"Cannot decode area. Continue in line {line_count}")
                        continue
                    # price_per_area = float(row[header_dict['trm2']])
                    extra_data = {
                        "floor_area": floor_area,
                        # "price_per_area": price_per_area
                    }
                    if phone not in user_dict:
                        if not phone:
                            admin_realtor = Realtor.objects.get(pk=1)
                            user_dict[phone] = admin_realtor
                        else:
                            new_user = User.objects.create_user(username=phone, password=default_password,
                                                                phone=phone, last_name=name[3:])
                            new_realtor = Realtor.objects.create(user=new_user)
                            user_dict[phone] = new_realtor
                    realtor = user_dict[phone]

                    if street in addr:
                        full_addr = f'{addr}, {district}'
                    else:
                        full_addr = f'{addr}, {street}, {district}'
                    full_addr = f'{full_addr}, Hà Nội'
                    title = f'{street} - {district} [{area} - {floor} - {lane_width}] [{price} tỷ]'
                    description = f"Khu vực {street} - {district}. Diện tích {area}."
                    if floor_code == 'c4' or floor_code == 'c' or floor_code == 'cap 4':
                        description += ' Nhà cấp 4.'
                    if floor > 1:
                        description += f' Nhà {floor} tầng.'
                    if house_type == HouseType.LAND:
                        description += ' Đất nền.'
                    elif house_type == HouseType.SHOP_HOUSE:
                        description += ' Kinh Doanh.'

                    if trans_type == TransactionType.PROJECT:
                        description += ' Dự án.'
                    if road_type == RoadType.ALLEY_CAR_2:
                        description += ' Nhà mặt phố.'
                    elif road_type == RoadType.ALLEY_TRIBIKE:
                        description += ' Ngõ 3 gác.'
                    elif road_type == RoadType.ALLEY_CAR:
                        description += ' Ngõ ô tô.'
                    elif road_type == RoadType.ALLEY_BIKE:
                        description += ' Ngõ xe máy.'

                    if code not in listing_obj:
                        if api_key:
                            geolocator = GeocodeEarth(api_key=api_key)
                            hanoi_bounds = ((21.097341, 105.929947), (20.920105, 105.702667))
                            location = geolocator.geocode(full_addr, boundary_rect=hanoi_bounds)
                        new_listing = Listing(realtor=realtor, code=code, status=status, street=street,
                                              address=full_addr, area=area, transaction_type=trans_type,
                                              house_type=house_type, road_type=road_type, list_date=created,
                                              direction=direction, price=price, sale_price=price,
                                              extra_data=extra_data, state=state, district=district_code,
                                              lane_width=lane_width, floors=int(floor), title=title,
                                              length=None, width=None)
                        if location and location.point:
                            listing_loc = Point(location.point.longitude, location.point.latitude)
                            new_listing.location = listing_loc
                        new_listing.save()
                        new_listings.append(new_listing)
                        listing_obj[code] = new_listing
                    else:
                        # Update WIP
                        # TODO
                        pass
    except Exception as ex:
        print(line_count)
        print_trace(ex)
