import csv
import datetime
import json
import logging
from decimal import Decimal

import pytz
from django.conf import settings
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.utils.text import slugify
from geopy import GeocodeEarth
from geopy.geocoders import Nominatim

from FunctionModule.accounts.models import User
from FunctionModule.cadastral.constants import district_data
from FunctionModule.listings.helpers import print_trace, get_house_type_short, get_short_title_from_house_type
from FunctionModule.listings.models import Listing, Status, TransactionType, HouseType, RoadType
from FunctionModule.realtors.models import Realtor

default_password = 'tgnpvn@2021'
logger = logging.getLogger(__name__)


def read_header(header_row, listing_type):
    if listing_type == 'K1':
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
            "don-vi": 9,
            "dac-diem": 10,
            "huong": 11,
            "dt": 14,
            "trm2": 15,
        }
    else:
        header_dict = {
            "dia-chi": 1,
            "dt": 2,
            "so-tang": 3,
            "mat-tien": 4,
            "gia": 5,
            "quan": 6,
            "dau-chu": 8,
            "sdt": 9,
            "hoa-hong": 10,
            "nguon": 11,
            "hien-trang": 12,
            "tgian": 13,
            "thanh-pho": 15,
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


def handle_import(file_path, listing_type):
    line_count = 0
    with open('saved_search.json', 'r', encoding='utf-8') as f:
        searched_locations = json.load(f)
    try:
        realtors = Realtor.objects.all()
        user_dict = {}
        for obj in realtors:
            user_dict[obj.user.phone] = obj

        listing_count = Listing.objects.count()
        limit = 1000
        listing_obj = {}
        api_key = getattr(settings, 'GEOEARTH_API_KEY', '')
        if listing_count>0:
         last_id = Listing.objects.latest('id').id
        else:
          last_id = 0

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

        with open(file_path, 'r', encoding="utf-8", errors='ignore') as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            new_listings = []
            updated_listings = []
            state_code = "01"
            hanoi_district_list = district_data[state_code]
            hanoi_districts = {}
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')

            for item in hanoi_district_list:  # type: dict
                hanoi_districts[item['name']] = item['code']
            for row in csv_reader:
                line_count += 1

                if line_count == 1:
                    header_dict = read_header(row,listing_type)
                district = row[header_dict['quan']]
                if not district:
                    logger.info(f"No district. Continue in line {line_count}")
                    continue
                if district in hanoi_districts:
                    district_code = hanoi_districts[district]
                else:
                    # logger.info(f"District code not found. Continue in line {line_count}")
                    continue
                try:
                    created = datetime.datetime.strptime(row[header_dict['tgian']], '%d/%m/%Y %H:%M:%S')
                    created = created.replace(tzinfo=timezone)
                except ValueError:
                    created = datetime.datetime.now(tz=timezone)
                name = row[header_dict['dau-chu']]
                phone = row[header_dict['sdt']]
                phone = phone.split(' ')[0]
                if not phone.isalnum():
                    logger.info(f"Phone invalid. Continue in line {line_count}")
                    continue
                if phone not in user_dict:
                    if not phone:
                        admin_realtor = Realtor.objects.get(pk=1)
                        user_dict[phone] = admin_realtor
                    else:
                        email = f'{phone}@gmail.com'
                        new_user = User.objects.create_user(username=phone, password=default_password,
                                                            phone=phone, email=email, last_name=name[3:])
                        new_realtor = Realtor.objects.create(user=new_user)
                        user_dict[phone] = new_realtor
                realtor = user_dict[phone]
                trans_type = TransactionType.SELL
                house_type = HouseType.TOWN_HOUSE
                road_type = RoadType.ALLEY_TRIBIKE
                direction = ""
                reward = 100
                bonus_rate = 3
                desc = ""

                try:
                    # area = float(row[header_dict['dt']].replace('c4', ''))
                    area = float(row[header_dict['dt']])
                except ValueError:
                    # logger.info(f"Cannot decode area. Continue in line {line_count}")
                    continue

                if listing_type == "K1":
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

                    addr = row[header_dict['dia-chi']].replace('.', '/').replace(',', '/')
                    street = row[header_dict['pho']]
                    # Hanoi
                    state = '01'
                    if street in addr:
                        full_addr = f'{addr}, {district}'
                    else:
                        full_addr = f'{addr}, {street}, {district}'
                    full_addr = f'{full_addr}, Hà Nội'

                    # billion vnd
                    price = row[header_dict['gia']]
                    if not price:
                        continue
                    if price == '#VALUE!':
                        continue
                    price = Decimal(price.replace(',', '.'))

                    desc = row[header_dict['dac-diem']]
                    if desc == 'Mặt Phố':
                        house_type = HouseType.STREET_HOUSE
                        road_type = RoadType.ALLEY_CAR_2
                    elif desc == 'Kinh Doanh':
                        house_type = HouseType.SHOP_HOUSE
                        road_type = RoadType.ALLEY_CAR
                    elif desc == 'Ngõ Ô Tô':
                        road_type = RoadType.ALLEY_CAR
                    elif desc == 'Ngõ 3 Gác':
                        road_type = RoadType.ALLEY_TRIBIKE
                    elif desc == 'Ngõ Xe Máy':
                        road_type = RoadType.ALLEY_BIKE
                    elif desc == 'Đất Dự Án':
                        house_type = HouseType.PLOT
                        road_type = RoadType.ALLEY_CAR_2
                        trans_type = TransactionType.PROJECT

                    encoded_num = row[header_dict['thong-so']]
                    splitter = encoded_num.split(' ')
                    splitter_len = len(splitter)
                    if splitter_len < 3:
                        # logger.info(f"Cannot decode encoded_num. Continue in line {line_count}")
                        continue
                    # splitter = list(filter(None, splitter))
                    floor_area = splitter[0].split('/')
                    if splitter_len == 2:
                        width = float(splitter[1].replace(',', '.'))
                    else:
                        try:
                            width = float(splitter[2].replace(',', '.'))
                        except ValueError:
                            # logger.info(f"Cannot decode floor_area. Continue in line {line_count}")
                            continue
                    floor = 0
                    floor_code = slugify(splitter[1].lower().replace('đ', 'd').replace('ấ', 'a').replace('t', ''))
                    if floor_code == 'C4' or floor_code == 'c' or floor_code == 'cap 4':
                        floor = 1
                        house_type = HouseType.TOWN_HOUSE
                    elif floor_code == 'da' or floor_code == 'd':
                        floor = 0
                        house_type = HouseType.LAND
                    else:
                        house_type = HouseType.TOWN_HOUSE
                        if splitter_len == 2:
                            floor = int(len(floor_area))
                        else:
                            try:
                                floor = int(floor_code)
                            except ValueError:
                                # logger.info(f"Cannot decode floor_code. Continue in line {line_count}")
                                continue
                    direction = get_direction(row[header_dict['huong']])

                    try:
                        price_per_area = float(price) / float(area) * 1000
                    except ValueError:
                        price_per_area = Decimal(row[header_dict['trm2']])
                        pass

                    don_vi = row[header_dict['don-vi']]
                elif listing_type == "K2":
                    status = row[header_dict['hien-trang']]
                    if not status:
                        status = Status.SELLING
                    else:
                        if status == 'Chuẩn' or status == 'Chờ duyệt' or status == 'Chim trời cá bể':
                            status = Status.SELLING
                        elif status == 'Tạm dừng bán':
                            status = Status.STOP_SELLING
                        elif status == 'Đã bán' or status == 'Đã cọc':
                            status = Status.SOLD
                        else:
                            status = Status.SALE

                    addr = row[header_dict['dia-chi']].replace('.', '/').replace('Số ', '').replace(' ', ' ')
                    so_nha = addr.split(' ')
                    lensonha = int(len(so_nha[0]))
                    street = addr[lensonha:]
                    state_name = row[header_dict['thanh-pho']]
                    full_addr = f'{addr}, {district}, {state_name}'

                    # billion vnd
                    price = Decimal(row[header_dict['gia']].split(' ')[0])
                    width = Decimal(row[header_dict['mat-tien']])
                    floor = float(row[header_dict['so-tang']])
                    if floor == 0:
                        house_type = HouseType.LAND
                    elif floor == 1:
                        house_type = HouseType.LOFT_HOUSE
                    else:
                        house_type = HouseType.TOWN_HOUSE

                    nguon = row[header_dict['nguon']]
                    hoa_hong = row[header_dict['hoa-hong']]
                    num_reward = float(hoa_hong.split(' ')[0])
                    if int(num_reward) > 3:
                        reward = num_reward
                    else:
                        bonus_rate = num_reward

                    don_vi = "Thiên Khôi"
                    extra_add = f' Nguồn {nguon}, hoa hồng {hoa_hong}.'

                    try:
                        price_per_area = float(price) / float(area) * 1000
                    except ValueError:
                        price_per_area = Decimal(row[header_dict['trm2']])
                        pass

                extra_data = f'Liên hệ với {name}, {phone}, {don_vi} để giao dịch. {extra_add}'
                starter = get_house_type_short(house_type)
                code = f'{starter}{created.strftime("%y%m")}{listing_type}{district_code}{int(area)}{int(floor)}{width}{price}'

                new_listing = Listing(realtor=realtor, code=code, status=status, street=street,
                                      address=full_addr, area=area, transaction_type=trans_type,
                                      house_type=house_type, road_type=road_type, list_date=created,
                                      direction=direction, price=price, reward_person=realtor,
                                      reward_person_mobile=phone, reward=reward, bonus_rate=bonus_rate,
                                      extra_data=extra_data, state=state_code, district=district_code,
                                      width=width, floors=int(floor), average_price=price_per_area, length=None, lane_width=None)
                title = f'Bán {get_short_title_from_house_type(new_listing.house_type)} {new_listing.street} {new_listing.district_name()} '
                if new_listing.area >= 30:
                    title += f'{new_listing.area:.0f}m '
                if new_listing.floors and new_listing.floors > 1:
                    title += f'{new_listing.floors} tầng '
                title += f'{new_listing.display_price}'
                title = title.upper()
                new_listing.title = title
                description = render_to_string('listings/defaultDescription.html',
                                               context={"listing": new_listing, "desc": desc})
                new_listing.description = description
                if full_addr in searched_locations:
                    if searched_locations[full_addr]:
                        listing_loc = Point(searched_locations[full_addr][1],
                                            searched_locations[full_addr][0])
                        new_listing.location = listing_loc
                # else:
                #     if api_key:
                #         geolocator = GeocodeEarth(api_key=api_key)
                #         #geolocator = Nominatim()
                #         hanoi_bounds = ((21.097341, 105.929947), (20.920105, 105.702667))
                #         location = geolocator.geocode(full_addr, boundary_rect=hanoi_bounds)
                #         if location and location.point:
                #             listing_loc = Point(location.point.longitude, location.point.latitude)
                #             new_listing.location = listing_loc
                #             searched_locations[full_addr] = [location.point.longitude,
                #                                              location.point.latitude]
                #         else:
                #             searched_locations[full_addr] = None

                if code in listing_obj:
                    t = Listing.objects.get(code=code)
                    t.is_published = new_listing.is_published
                    #t.title = new_listing.title
                    #t.description = new_listing.description
                    t.status = new_listing.status
                    t.price = new_listing.price
                    t.save()

                if code not in listing_obj:
                    new_listing.is_published = False
                    new_listing.save()
                    new_listings.append(new_listing)
                    listing_obj[code] = new_listing
                    del new_listing

    except Exception as ex:
        print(f"Error occurred at line: {line_count}")
        print(type(ex))
        print_trace(ex)
    finally:
        print(f'Read {line_count} lines')
        with open('saved_search.json', 'w', encoding='utf-8') as f:
            json.dump(searched_locations, f, ensure_ascii=False)
