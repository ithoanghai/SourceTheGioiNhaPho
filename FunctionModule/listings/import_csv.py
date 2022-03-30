import csv
import datetime
import json
import logging
import string
from decimal import Decimal
from string import digits

import pytz
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.text import slugify
from geopy import GeocodeEarth
from geopy.geocoders import Nominatim
from oauthlib.uri_validate import reserved

from FunctionModule.accounts.models import User
from FunctionModule.cadastral.constants import district_data
from FunctionModule.listings.helpers import print_trace, get_house_type_short, get_short_title_from_house_type
from FunctionModule.listings.models import Listing, Status, TransactionType, HouseType, RoadType
from FunctionModule.realtors.models import Realtor

default_password = 'tgnpvn@2021'
logger = logging.getLogger(__name__)


def read_header(header_row, listing_type):
    if listing_type == 'K1':
        logger.info(f"listing_type {listing_type} Nha Pho VN")
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
    elif listing_type == 'K2':
        logger.info(f"listing_type {listing_type} Thien Khoi")
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
            header_dict = read_header(next(csv_reader), listing_type)
            new_listings = []
            updated_listings = []
            state_code = "01"
            hanoi_district_list = district_data[state_code]
            hanoi_districts = {}
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            row_count = 0

            for item in hanoi_district_list:  # type: dict
                hanoi_districts[item['name']] = item['code']

            for row in reversed(list(csv_reader)):
                row_count += 1
                line_count = csv_reader.line_num - row_count + 1
                district = row[header_dict['quan']]
                if not district:
                    logger.info(f"No district. Continue in line {line_count}")
                    continue
                if district in hanoi_districts:
                    district_code = hanoi_districts[district]
                else:
                    # logger.info(f"District code not found. Continue in line {line_count}")
                    continue

                trans_type = TransactionType.SELL
                house_type = HouseType.TOWN_HOUSE
                road_type = RoadType.ALLEY_TRIBIKE_BIKE
                direction = ""
                reward = 100
                bonus_rate = 3
                desc = ""
                name = row[header_dict['dau-chu']]

                if listing_type == "K1":
                    try:
                        created = datetime.datetime.strptime(row[header_dict['tgian']], '%d/%m/%Y %H:%M:%S')
                        created = created.replace(tzinfo=timezone)
                    except ValueError:
                        created = datetime.datetime.now(tz=timezone)
                    status = row[header_dict['hien-trang']]
                    if not status:
                        status = Status.SELLING
                        published = True
                    else:
                        if status == 'Hạ chào':
                            status = Status.SALE
                            published = True
                        elif status == 'Còn bán':
                            status = Status.SELLING
                            published = True
                        elif status == 'Đã bán':
                            status = Status.SOLD
                            published = False
                        elif status == 'Dừng bán':
                            status = Status.STOP_SELLING
                            published = False

                    addr = row[header_dict['dia-chi']].replace('.', '/').replace(',', '/')
                    street = row[header_dict['pho']]
                    deep_address = addr.split('/')
                    # Hanoi
                    state = '01'
                    if street in addr:
                        full_addr = f'{addr}, {district}'
                    else:
                        full_addr = f'{addr}, {street}, {district}'
                    full_addr = f'{full_addr}, Hà Nội'
                    full_addr = full_addr.replace('CCCC', 'Chung cư cao cấp').replace('CCMN', 'Chung cư mini').replace('CC ', 'Chung cư ').replace(' , ', ', ')

                    # billion vnd
                    price = row[header_dict['gia']]
                    if not price:
                        continue
                    if price == '#VALUE!':
                        continue
                    price = Decimal(price.replace(',', '.'))

                    encoded_num = row[header_dict['thong-so']].replace('  ', ' ')
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
                    try:
                        area_p1 = splitter[0].split('/')
                        area_p2 = area_p1[0].split('(')
                        area_tmp = area_p2[0].split('\\')
                        if area_tmp[0] == 'Đất' or area_tmp[0] == 'đất':
                            area_tmp = splitter[1].replace(',', '.')
                        # area = float(row[header_dict['dt']].replace('c4', ''))
                        area = Decimal(row[header_dict['dt']].replace('Đất', area_tmp[0]).replace('đất', area_tmp[0]).replace('#VALUE!', area_tmp[0]).replace(',', '.').replace(' ', ''))
                    except ValueError:
                        area = Decimal(area_tmp[0].replace(',', '.').replace(' ', ''))
                        continue

                    floor = 0
                    floor_code = slugify(splitter[1].lower().replace('đ', 'd').replace('ấ', 'a').replace('t', '').replace('4', '').replace(' ', ''))
                    if floor_code == 'c' or floor_code == 'cap':
                        floor = 1
                        house_type = HouseType.LOFT_HOUSE
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

                    shop_house = "shophouse"
                    biet_thu = "bt"
                    lien_ke = "lk"
                    dich_vu = "dv"
                    thap_tang = "tt"
                    lo = "lô"
                    chung_cu = "chung cư"
                    cao_tang = "ct"
                    tap_the = "tập thể"
                    du_an = "dự án"
                    desc = row[header_dict['dac-diem']]
                    if desc == 'Mặt Phố' or (len(deep_address) == 1 and price > 6):
                        house_type = HouseType.STREET_HOUSE
                        road_type = RoadType.ALLEY_CAR_2
                        if price > 30:
                            published = False
                    elif desc == 'Ngõ Ô Tô':
                        road_type = RoadType.ALLEY_CAR
                    elif desc == 'Ngõ 3 Gác':
                        road_type = RoadType.ALLEY_TRIBIKE_BIKE
                    elif desc == 'Ngõ Xe Máy':
                        road_type = RoadType.ALLEY_BIKE
                    elif desc == 'Đất Dự Án':
                        house_type = HouseType.PLOT
                        road_type = RoadType.ALLEY_CAR_2
                        trans_type = TransactionType.PROJECT
                    elif shop_house in full_addr.lower() or desc == 'Kinh Doanh':
                        house_type = HouseType.SHOP_HOUSE
                        road_type = RoadType.ALLEY_CAR_2
                    if biet_thu in full_addr.lower():
                        house_type = HouseType.VILLA
                        road_type = RoadType.ALLEY_CAR_2
                    elif lien_ke in full_addr.lower() or dich_vu in full_addr.lower() or lo in full_addr.lower() or du_an in full_addr.lower() or desc == 'Liền Kề' or thap_tang in full_addr.lower():
                        house_type = HouseType.PLOT
                        road_type = RoadType.ALLEY_CAR_2
                    elif cao_tang in full_addr.lower() or chung_cu in full_addr.lower() or " tt " in full_addr.lower() or tap_the in full_addr.lower():
                        full_addr = full_addr.replace(' TT ', ' tập thể ').replace('CCCC', 'Chung cư cao cấp')
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR_2
                    elif "chung cư mini" in full_addr.lower():
                        full_addr = full_addr.replace('CCMN', 'Chung cư Mini')
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR_TRIBIKE

                    direction = get_direction(row[header_dict['huong']])

                    don_vi = row[header_dict['don-vi']]
                    extra_add = f' Nguồn {name}, hoa hồng 3%, hỏi lại đầu chủ cho chính xác.'
                elif listing_type == "K2":
                    try:
                        created = datetime.datetime.strptime(row[header_dict['tgian']], '%d/%m/%Y %H:%M')
                        created = created.replace(tzinfo=timezone)
                    except ValueError:
                        created = datetime.datetime.now(tz=timezone)
                    try:
                        # area = float(row[header_dict['dt']].replace('c4', ''))
                        area = Decimal(row[header_dict['dt']].replace(',', '.'))
                    except ValueError:
                        pass

                    status = row[header_dict['hien-trang']]
                    if not status:
                        status = Status.SELLING
                        published = True
                    else:
                        if status == 'Chuẩn' or status == 'Chờ duyệt' or status == 'Chim trời cá bể':
                            status = Status.SELLING
                            published = True
                        elif status == 'Tạm dừng bán':
                            status = Status.STOP_SELLING
                            published = False
                        elif status == 'Đã bán' or status == 'Đã cọc':
                            status = Status.SOLD
                            published = False
                        else:
                            status = Status.SALE
                            published = True

                    addr = row[header_dict['dia-chi']].replace('.', '/').replace('Số ', '').replace(' ', ' ')
                    so_nha = addr.split(' ')
                    lensonha = int(len(so_nha[0]))
                    street = addr[lensonha:].replace('(', '').replace(')', '').replace('/', '').replace('  ', '')
                    remove_digits = street.maketrans('', '', digits)
                    street = street.translate(remove_digits)
                    addr = addr.replace(' TT ', ' tập thể ').replace('CCCC', 'Chung cư cao cấp').replace('CCMN', 'Chung cư mini').replace('CC ', 'Chung cư ')
                    state_name = row[header_dict['thanh-pho']]
                    full_addr = f'{addr}, {district}, {state_name}'

                    # billion vnd
                    try:
                        if (not (row[header_dict['gia']].split(' ')[0] and row[header_dict['gia']].split(' ')[0].strip())):
                            continue
                        price = Decimal(row[header_dict['gia']].split(' ')[0])
                    except ValueError:
                        logger.info(f"price {price}")
                        continue

                    width = Decimal(row[header_dict['mat-tien']])
                    floor = float(row[header_dict['so-tang']])

                    if floor == 0:
                        house_type = HouseType.LAND
                    elif floor == 1:
                        house_type = HouseType.LOFT_HOUSE
                    else:
                        house_type = HouseType.TOWN_HOUSE

                    deep_address = so_nha[0].split('/')
                    shop_house = "shophouse"
                    biet_thu = "bt"
                    lien_ke = "lk"
                    thap_tang = "tt"
                    dich_vu = "dv"
                    lo = "lô"
                    chung_cu = "chung cư"
                    cao_tang = "ct"
                    tap_the = "tập thể"
                    du_an = "dự án"
                    if len(deep_address) == 1 and price > 6:
                        house_type = HouseType.STREET_HOUSE
                        road_type = RoadType.ALLEY_CAR_2
                        if price > 30:
                            published = False
                    elif shop_house in full_addr.lower():
                        house_type = HouseType.SHOP_HOUSE
                        road_type = RoadType.ALLEY_CAR_2
                    if biet_thu in full_addr.lower():
                        house_type = HouseType.VILLA
                        road_type = RoadType.ALLEY_CAR_2
                    elif lien_ke in full_addr.lower() or dich_vu in full_addr.lower() or lo in full_addr.lower() or du_an in full_addr.lower() or desc == 'Liền Kề' or thap_tang in full_addr.lower():
                        house_type = HouseType.PLOT
                        road_type = RoadType.ALLEY_CAR_2
                    elif cao_tang in full_addr.lower() or chung_cu in full_addr.lower() or tap_the in full_addr.lower():
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR_2
                    elif "chung cư mini" in full_addr.lower():
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR

                    nguon = row[header_dict['nguon']]
                    hoa_hong = row[header_dict['hoa-hong']]
                    num_reward = 100
                    if (not (hoa_hong.split(' ')[0] and hoa_hong.split(' ')[0].strip())):
                        num_reward = 100
                        bonus_rate = 3
                    if 3 < int(num_reward) < 10000:
                        reward = num_reward
                    elif int(num_reward) > 0:
                        bonus_rate = num_reward
                    else:
                        bonus_rate = 3

                    don_vi = "Thiên Khôi"
                    extra_add = f' Nguồn {nguon}, hoa hồng {hoa_hong}.'
                try:
                    if price > 1000000 and area < 10000000:
                        price = Decimal(price / 1000000)
                    elif price > 100000 and area < 1000000:
                        price = Decimal(price / 100000)
                    elif price > 10000 and area < 100000:
                        price = Decimal(price / 10000)
                    elif price > 1000 and area < 10000:
                        price = Decimal(price / 1000)
                    if float(area) > 0:
                        price_per_area = Decimal(float(price) / float(area) * 1000)
                    else:
                        price_per_area = None
                except ValueError:
                    pass

                phone = row[header_dict['sdt']]
                phone = phone.split(' ')[0]
                phone = phone.split('-')[0]
                extra_data = f'Liên hệ với {name}, {phone}, {don_vi} để giao dịch. {extra_add}'
                if not phone.isalnum():
                    logger.info(f"Phone invalid. Continue in line {line_count}")
                    continue
                tmp_phone = phone
                if phone not in user_dict:
                    if not phone:
                        admin_realtor = Realtor.objects.get(pk=1)
                        user_dict[phone] = admin_realtor
                    else:
                        if len(phone) == 9:
                            query = Q(phone=phone) | Q(phone=f'0{phone}')
                            usr = User.objects.filter(query)
                            phone = f'0{phone}'
                            email = f'{phone}@gmail.com'
                            extra_data = f'Liên hệ với {name}, {phone}, {don_vi} để giao dịch. {extra_add}'
                            bio = f'{name}, {phone}, {don_vi}.'
                            if usr.exists():
                                usr.username = phone
                                usr.phone = phone
                                usr.last_name = name
                                usr.update()
                                #print(f"update user: {usr}")
                            else:
                                new_user = User.objects.create_user(username=phone, password=default_password,
                                                                    phone=phone, email=email, last_name=name, bio=bio)
                                new_realtor = Realtor.objects.create(user=new_user)
                                user_dict[phone] = new_realtor
                                #print(f"new_user: {new_user}")
                        else:
                            extra_data = f'Liên hệ với {name}, {phone}, {don_vi} để giao dịch. {extra_add}'
                            bio = f'{name}, {phone}, {don_vi}.'
                            email = f'{phone}@gmail.com'
                            new_user = User.objects.create_user(username=phone, password=default_password,
                                                                phone=phone, email=email, last_name=name, bio=bio)
                            new_realtor = Realtor.objects.create(user=new_user)
                            user_dict[phone] = new_realtor
                elif len(phone) == 9 and user_dict.get(f'0{phone}') is None:
                    query = Q(phone=phone) | Q(phone=f'0{phone}')
                    usr = User.objects.get(query)
                    phone = f'0{phone}'
                    email = f'{phone}@gmail.com'
                    bio = f'{name}, {phone}, {don_vi}.'
                    if usr is not None:
                        usr.username = phone
                        usr.phone = phone
                        usr.last_name = name
                        usr.email = email
                        usr.bio = bio
                        usr.save()
                        if user_dict.get(tmp_phone) is not None:
                            user_dict[tmp_phone].user = usr
                        print(f"update user: {usr}")

                if user_dict.get(tmp_phone) is not None:
                    realtor = user_dict[tmp_phone]
                else:
                    realtor = user_dict[phone]

                starter = get_house_type_short(house_type)
                code = f'{starter}{created.strftime("%y%m")}{listing_type}{district_code}{int(area)}{int(floor)}{width}{price}'
                #008 Q. Hoàng Mai,009 Q. Thanh Xuân, 020 H. Thanh Trì, 278 H. Thanh Oai, 268 Q. Hà Đông
                if district_code == '008' or district_code == '009' or district_code == '020' or district_code == '278' or district_code == '268':
                    priority = 8
                    if price < 50 or status == Status.SELLING:
                        published = True
                    else:
                        published = False
                else:
                    priority = 9
                    published = False

                new_listing = Listing(realtor=realtor, code=code, status=status, street=street,
                                      address=full_addr, area=area, transaction_type=trans_type,
                                      house_type=house_type, road_type=road_type, list_date=created,
                                      direction=direction, price=price, reward_person=realtor, priority=priority,
                                      reward_person_mobile=phone, reward=reward, bonus_rate=bonus_rate,
                                      extra_data=extra_data, state=state_code, district=district_code, is_published=published,
                                      width=width, floors=floor, average_price=price_per_area, length=None, lane_width=None)
                title = f'Bán {get_short_title_from_house_type(new_listing.house_type)} {new_listing.street} {new_listing.district_name()} '

                if new_listing.area >= 30:
                    title += f'{new_listing.area:.0f}m '
                if new_listing.floors and new_listing.floors > 1:
                    title += f'{new_listing.floors:.0f} tầng '
                title += f'{new_listing.display_price}'
                title = title.upper().replace('  ', ' ')
                new_listing.title = title
                description = render_to_string('listings/defaultDescription.html',
                                               context={"listing": new_listing, "desc": desc})
                new_listing.description = description
                new_listing.description = new_listing.description.replace('  ', ' ')
                new_listing.is_published = new_listing.is_published
                if full_addr in searched_locations:
                    if searched_locations[full_addr]:
                        listing_loc = Point(searched_locations[full_addr][0],
                                            searched_locations[full_addr][1])
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
                    queryset_list = Listing.objects.filter(code=code)
                    if queryset_list.exists():
                        f = queryset_list.first()
                        if f.priority == 1 or f.priority == 2:
                            f.status = new_listing.status
                            f.is_published = new_listing.is_published
                            f.save()
                            logger.info(f"row {line_count}: chỉ cập nhật {code} đã biên tập dữ liệu, từ trạng thái {f.status} sang {new_listing.status}")
                        else:
                            f.house_type = new_listing.house_type
                            f.road_type = new_listing.road_type
                            f.status = new_listing.status
                            f.area = new_listing.area
                            f.floors = new_listing.floors
                            f.width = new_listing.width
                            f.price = new_listing.price
                            f.list_date = new_listing.list_date
                            f.reward_person_mobile = new_listing.reward_person_mobile
                            f.extra_data = new_listing.extra_data
                            f.priority = new_listing.priority
                            f.is_published = new_listing.is_published
                            f.save()
                            logger.info(f"row {line_count}: update {code}, district {district_code} publish is {f.is_published} to {published}")
                else:
                    queryset_list = Listing.objects.filter(address=new_listing.address,price=new_listing.price, district=new_listing.district, area=new_listing.area,
                                                           floors=new_listing.floors).order_by('-list_date')
                    if queryset_list.exists():
                        listing = queryset_list.first()
                        if listing.priority == 1 or listing.priority == 2:
                            listing.status = new_listing.status
                            listing.is_published = new_listing.is_published
                            listing.save()
                            logger.info(
                                f"row {line_count}: cập nhật bđs đã có nhưng ko tìm thấy code {code} đã biên tập dữ liệu, từ trạng thái {listing.status} sang {new_listing.status}")
                        else:
                            listing.is_published = new_listing.is_published
                            listing.house_type = new_listing.house_type
                            listing.road_type = new_listing.road_type
                            listing.status = new_listing.status
                            listing.area = new_listing.area
                            listing.floors = new_listing.floors
                            listing.width = new_listing.width
                            listing.price = new_listing.price
                            listing.list_date = new_listing.list_date
                            listing.reward_person_mobile = new_listing.reward_person_mobile
                            listing.extra_data = new_listing.extra_data
                            listing.priority = new_listing.priority
                            code_old = listing.code
                            listing.code = new_listing.code
                            listing.save()
                            logger.info(f"row {line_count}: cập nhật listing code {code_old} sang {listing.code}")
                        # for ite in queryset_list[1:]:
                        #     ite.delete()
                        #     logger.info(f"row {line_count}: xóa mã {listing.code} trùng")
                    else:
                        new_listing.save()
                        new_listings.append(new_listing)
                        listing_obj[code] = new_listing
                        print(f"row {line_count}: new listing: {new_listing}")
                        del new_listing

        # đoạn code phục vụ
        # f = Listing.objects.filter(is_published=True)
        # for r in f:
        #     if r.priority == 1 or r.priority == 2:
        #         r.is_published = True
        #     elif r.price > 50 or r.status == 'sold' or r.status == 'stop_selling':
        #         r.is_published = False
        #     # 008 Q. Hoàng Mai,009 Q. Thanh Xuân, 020 H. Thanh Trì, 278 H. Thanh Oai, 268 Q. Hà Đông
        #     elif r.district == '008' or r.district == '009' or r.district == '020' or r.district == '278' or r.district == '268':
        #         r.is_published = True
        #     else:
        #         r.is_published = False
        #     r.save()
        #     print(f"cập nhật hiển thị cho {r.code}")

    except Exception as ex:
        print(f"Error occurred at line: {line_count}")
        print(type(ex))
        print_trace(ex)
    finally:
        print(f'Read {line_count} lines')
        with open('saved_search.json', 'w', encoding='utf-8') as f:
            json.dump(searched_locations, f, ensure_ascii=False)
