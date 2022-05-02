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
            "tieude": 1,
            "mota": 2,
            "mota-dauchu": 3,
            "anh-nha": 4,
            "anh-so": 5,
            "hien-trang": 6,
            "dia-chi": 7,
            "pho": 8,
            "quan": 9,
            "thong-so": 10,
            "gia": 11,
            "dau-chu": 12,
            "sdt": 13,
            "don-vi": 14,
            "dac-diem": 15,
            "huong": 16,
            "dt": 19,
            "trm2": 20,
            "hoa-hong": 21,
            "nguon": 22,
            "thanh-pho": 23
        }
    elif listing_type == 'K2':
        logger.info(f"listing_type {listing_type} Thien Khoi")
        header_dict = {
            "tieude": 1,
            "mota": 2,
            "mota-dauchu": 3,
            "anh-nha": 4,
            "anh-so": 5,
            "dia-chi": 6,
            "dt": 7,
            "so-tang": 8,
            "mat-tien": 9,
            "gia": 10,
            "quan": 11,
            "dau-chu": 13,
            "sdt": 14,
            "hoa-hong": 15,
            "nguon": 16,
            "hien-trang": 17,
            "tgian": 18,
            "thanh-pho": 20,
            "don-vi": 21,
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


def handle_import(request, file_path, listing_type):
    line_count = 0
    with open('saved_search.json', 'r', encoding='utf-8') as f:
        searched_locations = json.load(f)
    try:
        if request.user is not None:
            user = request.user
            real = Realtor.objects.filter(user=user)
            if real.first() is None:
                Realtor.objects.create(user=user)

    # realtor scan and reorder
        realtors = Realtor.objects.all()
        user_dict = {}
        for obj in realtors:
            if len(obj.user.phone) == 9 or len(obj.user.phone) == 10:
                user_dict[obj.user.phone] = obj
            else:
                queryset_list = Listing.objects.filter(realtor=obj)
                usr_list = User.objects.filter(last_name=obj.user.last_name)
                fone = obj.user.phone
                for usr in usr_list:
                    if len(usr.phone) == 10:
                        fone = usr.phone
                for listing in queryset_list:
                    if len(fone) == 10 or len(fone) == 9:
                        usr = User.objects.get(phone=fone)
                        print(f"user: {usr}")
                        rel = Realtor.objects.filter(user__phone=fone)
                        print(f"realtor: {rel}")
                        listing.realtor = rel
                        listing.save()
                        print(f"cập nhật listing có realtor lỗi sang realtor đầy đủ: {listing.realtor}, phone {fone}")
                    else:
                        listing.delete()
                        print(f"xóa listing rác do không có realtor phù hợp: {listing}")

                obj.delete()
                usr = User.objects.get(phone=obj.user.phone)
                usr.delete()
                print(f"Xóa realtor và rác: {obj}, có phone {obj.user.phone}")

        listing_count = Listing.objects.count()
        limit = 1000
        listing_obj = {}
        api_key = getattr(settings, 'GEOEARTH_API_KEY', '')
        if listing_count>0:
         last_id = Listing.objects.latest('id').id
        else:
          last_id = 0

    #realtor scan and reorder
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

    # get a list of all districts in Hanoi
        state_code = "01"
        hanoi_district_list = district_data[state_code]
        hanoi_districts = {}
        for item in hanoi_district_list:  # type: dict
            hanoi_districts[item['name']] = item['code']

    #Open the listing file and import it into the system
        with open(file_path, 'r', encoding="utf-8", errors='ignore') as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            header_dict = read_header(next(csv_reader), listing_type)
            new_listings = []
            updated_listings = []
            timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            row_count = 0

        #start reading and scanning the file from the bottom up
            for row in reversed(list(csv_reader)):
                row_count += 1
                line_count = csv_reader.line_num - row_count + 1
                trans_type = TransactionType.SELL
                house_type = HouseType.TOWN_HOUSE
                road_type = RoadType.ALLEY_TRIBIKE_BIKE
                direction = ""
                reward = 100
                bonus_rate = 3
                desc = ""
                name = row[header_dict['dau-chu']]
                realtor = Realtor.objects.filter(pk=1).first()

                #read state, district information
                state_name = row[header_dict['thanh-pho']]
                if not state_name:
                    # Hanoi
                    state_name = 'Hà Nội'
                district = row[header_dict['quan']]
                if not district:
                    logger.info(f"No district. Continue in line {line_count}")
                    continue
                if district in hanoi_districts:
                    district_code = hanoi_districts[district]
                else:
                    # logger.info(f"District code not found. Continue in line {line_count}")
                    continue

                #Read information about date and time listing
                created_date = row[header_dict['tgian']]
                try:
                    if listing_type == "K1":
                        created = datetime.datetime.strptime(created_date, '%d/%m/%Y %H:%M:%S')
                    elif listing_type == "K2":
                        created = datetime.datetime.strptime(created_date, '%d/%m/%Y %H:%M')
                    created = created.replace(tzinfo=timezone)
                except ValueError:
                    logger.info(f"error date create {created_date}")
                    created = datetime.datetime.now(tz=timezone)

                #Read information about real estate
                area = row[header_dict['dt']]
                try:
                    # area = float(row[header_dict['dt']].replace('c4', ''))
                    area = Decimal(area.replace(',', '.').replace(' ', ''))
                except ValueError:
                    logger.info(f"error area  {area}")
                    pass

                # Read real estate price information
                price = row[header_dict['gia']]
                try:
                    price = Decimal(price.split(' ')[0].strip().replace(',', '.'))
                    if not price or price == '#VALUE!':
                        continue
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
                    logger.info(f"error price {price}")
                    pass

                # Read information about the current state of the sale and set priority, show/hide into web by district
                status = row[header_dict['hien-trang']]
                try:
                    if status == 'Còn bán' or status == 'Chuẩn' or status == 'Chờ duyệt' or status == 'Chim trời cá bể':
                        status = Status.SELLING
                    elif status == 'Đã bán' or status == 'Đã cọc':
                        status = Status.SOLD
                    elif status == 'Dừng bán' or status == 'Tạm dừng bán':
                        status = Status.STOP_SELLING
                    elif status == 'Hạ chào':
                        status = Status.SALE
                    else:
                        status = Status.SOLD
                    # 008 Q. Hoàng Mai,009 Q. Thanh Xuân, 020 H. Thanh Trì, 278 H. Thanh Oai, 268 Q. Hà Đông
                    if district_code == '008' or district_code == '009' or district_code == '020' or district_code == '278' or district_code == '268':
                        priority = 8
                        if status == Status.SELLING:
                            is_published = True
                        else:
                            is_published = False
                    else:
                        priority = 9
                        is_published = False

                except ValueError:
                    logger.info(f"error status {status}")
                    pass

                #read đơn vị
                try:
                    don_vi = row[header_dict['don-vi']]
                    if don_vi is None:
                        don_vi = "Thiên Khôi"
                except ValueError:
                    don_vi = "Thiên Khôi"

                #read nguồn & hoa hồng
                try:
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
                    if nguon is not None:
                        extra_add = f' Nguồn {nguon}, hoa hồng {hoa_hong}.'
                    else:
                        extra_add = f' Nguồn nhà phố, hoa hồng 3%, xác minh lại với đầu chủ {name}.'
                except ValueError:
                    extra_add = f' Nguồn nhà phố, hoa hồng 3%, xác minh lại với đầu chủ {name}.'

                #Read information about specialist phone number
                try:
                    phone = row[header_dict['sdt']]
                    phone = phone.split(' ')[0]
                    phone = phone.split('-')[0]
                    if not phone.isalnum():
                        admin_realtor = Realtor.objects.filter(pk=1)
                        user_dict[phone] = admin_realtor.first()
                        logger.info(f"Phone invalid. Continue in line {line_count}")
                        continue
                    else:
                        # update, delete user, realtor
                        tmp_phone = phone
                        if len(phone) == 9:
                            phone = f'0{phone}'
                        extra_data = f'Liên hệ với {name}, {phone}, {don_vi} để giao dịch. {extra_add}'
                        if phone not in user_dict and len(phone) == 10:
                            if not phone:
                                admin_realtor = Realtor.objects.get(pk=1)
                                user_dict[phone] = admin_realtor
                                print(f"user_dict[phone]: {admin_realtor}")
                            else:
                                query = Q(phone=phone) | Q(phone=tmp_phone) | Q(last_name=name)
                                querylist_usr = User.objects.filter(query)
                                email = f'{phone}@gmail.com'
                                if querylist_usr.exists():
                                    usr = querylist_usr.first()
                                    usr.username = phone
                                    usr.last_name = name
                                    if usr.phone == phone:
                                        extra_phone = {phone}
                                    else:
                                        extra_phone = f'{usr.phone} hoặc {phone}'
                                    usr.phone = phone
                                    usr.bio = f'{name}, {extra_phone}, {don_vi}.'
                                    usr.save()
                                    query = Q(user__phone=phone) | Q(user__phone=tmp_phone) | Q(user__last_name=name)
                                    user_dict[phone] = Realtor.objects.filter(query).first()
                                    if user_dict[phone] is None:
                                        new_realtor = Realtor.objects.create(user=usr)
                                        user_dict[phone] = new_realtor
                                    extra_data = f'Liên hệ với {name}, {extra_phone}, {don_vi} để giao dịch. {extra_add}'
                                    print(f"update user: {usr}")
                                else:
                                    new_user = User.objects.create_user(username=phone, password=default_password,
                                                                        phone=phone, email=email, last_name=name, bio=bio)
                                    new_user.save()
                                    new_realtor = Realtor.objects.create(user=new_user)
                                    user_dict[phone] = new_realtor
                                    print(f"new_user: {new_user}")
                            realtor = user_dict[phone]
                        elif user_dict.get(phone) and len(phone) == 10:
                            query = Q(phone=phone) | Q(phone=tmp_phone)
                            usrs = User.objects.filter(query)
                            email = f'{phone}@gmail.com'
                            bio = f'{name}, {phone}, {don_vi}.'
                            for usr in usrs:
                                if usr.phone != tmp_phone:
                                    usr.username = phone
                                    usr.phone = phone
                                    usr.last_name = name
                                    usr.email = email
                                    usr.bio = bio
                                    usr.save()
                                    #print(f"cập nhật user: {usr}")
                            if len(phone) == 10 and len(tmp_phone) == 10:
                                dt = phone[1:]
                                if user_dict.get(dt) is not None:
                                    realtor_tmp = user_dict[dt]
                                    queryset_list = Listing.objects.filter(realtor=realtor_tmp).order_by('-list_date')
                                    for listing in queryset_list:
                                        listing.realtor = user_dict[phone]
                                        listing.save()
                                    if realtor_tmp is not None:
                                        realtor_list = Realtor.objects.filter(user__phone__contains=dt)
                                        if realtor_list.count() > 1:
                                            realtor_tmp.delete()
                                            usr_list = User.objects.filter(phone=dt)
                                            for usr in usr_list:
                                                if len(usr.phone) == 9:
                                                    usr.delete()
                                            user_dict[dt].clean()
                                            print(f"Xóa realtor và user rác kho K1: {realtor_tmp}, phone {dt}")

                            realtor = user_dict[phone]
                        elif len(phone) != 10:
                            if user_dict.get(phone):
                                realtor_tmp = user_dict[phone]
                                queryset_list = Listing.objects.filter(realtor=realtor_tmp).order_by('-list_date')
                                usr_list = User.objects.filter(phone__contains=phone)
                                for usr in usr_list:
                                    if len(usr.phone) == 10:
                                        for listing in queryset_list:
                                            listing.realtor = user_dict[usr.phone]
                                            realtor = user_dict[usr.phone]
                                            listing.save()
                                if realtor_tmp is not None:
                                    realtor_tmp.delete()
                                    user_dict[phone].clean()
                                    usr = User.objects.get(phone=phone)
                                    usr.delete()
                                    print(f"Xóa realtor và user rác : {realtor_tmp}, phone {phone}")
                                if realtor is None:
                                    realtor = Realtor.objects.get(pk=1)
                            elif phone not in user_dict:
                                usr_list = User.objects.filter(last_name=name)
                                for usr in usr_list:
                                    if len(usr.phone) == 10:
                                        realtor = usr.realtor
                except ValueError:
                    logger.info(f"error phone {phone}")

                if listing_type == "K0":
                    logger.info(f"import data from TGNP template")
                elif listing_type == "K1":
                    addr = row[header_dict['dia-chi']].replace('.', '/').replace(',', '/')
                    street = row[header_dict['pho']]
                    deep_address = addr.split('/')

                    if street in addr:
                        full_addr = f'{addr}, {district}'
                    else:
                        full_addr = f'{addr}, {street}, {district}'
                    full_addr = f'{full_addr}, Hà Nội'
                    full_addr = full_addr.replace('CCCC', 'Chung cư cao cấp').replace('CCMN', 'Chung cư mini').replace('CC ', 'Chung cư ').replace(' , ', ', ')
                    add_search_map = f'{deep_address[0]}, {street}, {district}, {state_name}'

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

                elif listing_type == "K2":
                    addr = row[header_dict['dia-chi']].replace('.', '/').replace('Số ', '').replace(' ', ' ')
                    addr = addr.replace(' TT ', ' tập thể ').replace('CCCC', 'Chung cư cao cấp').replace('CCMN', 'Chung cư mini').replace('CC ', 'Chung cư ')
                    so_nha = addr.split(' ')
                    lensonha = int(len(so_nha[0]))
                    deep_address = so_nha[0].split('/')
                    street = addr[lensonha:].replace('(', '').replace(')', '').replace('/', '').replace('  ', ' ')
                    street = street.translate(street.maketrans('', '', digits))
                    full_addr = f'{addr}, {district}, {state_name}'
                    add_search_map = f'{deep_address[0]}, {street}, {district}, {state_name}'
                    add_search_map = add_search_map.replace('  ', ' ')

                    width = Decimal(row[header_dict['mat-tien']])
                    floor = float(row[header_dict['so-tang']])

                    if floor == 0:
                        house_type = HouseType.LAND
                    elif floor == 1:
                        house_type = HouseType.LOFT_HOUSE
                    else:
                        house_type = HouseType.TOWN_HOUSE

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

                # search location on map
                listing_loc = Point(105.83549388560711, 20.976795401917798)
                if add_search_map in searched_locations:
                    if searched_locations[add_search_map]:
                        listing_loc = Point(searched_locations[full_addr][0],
                                            searched_locations[full_addr][1])
                        logger.info(f"listing_loc search ok {searched_locations[full_addr][0]} , {searched_locations[full_addr][1]}")
                else:
                    #if api_key:
                    #geolocator = GeocodeEarth(api_key=api_key)
                    geolocator = Nominatim(user_agent="thegioinhaphovietnam.com.vn")
                    #GeocodeEarth.geocoders.options.default_user_agent = "my-application"
                    hanoi_bounds = ((21.097341, 105.929947), (20.920105, 105.702667))
                    location = geolocator.geocode(add_search_map, bounded=True, viewbox=hanoi_bounds)
                    if location and location.point:
                        listing_loc = Point(location.point.longitude, location.point.latitude)
                        searched_locations[full_addr] = [location.point.longitude,
                                                         location.point.latitude]
                    else:
                        searched_locations[full_addr] = None

                starter = get_house_type_short(house_type)
                code = f'{starter}{created.strftime("%y%m")}{listing_type}{district_code}{int(area)}{int(floor)}{width}{price}'
                new_listing = Listing(user=user, realtor=user.realtor, code=code, status=status, street=street,
                                      address=full_addr, area=area, transaction_type=trans_type,
                                      house_type=house_type, road_type=road_type, list_date=created,
                                      direction=direction, price=price, reward_person=realtor.user.name, priority=priority,
                                      reward_person_mobile=realtor.user.phone, reward=reward, bonus_rate=bonus_rate,
                                      extra_data=extra_data, state=state_code, district=district_code, is_published=is_published,
                                      width=width, floors=floor, average_price=price_per_area, length=None, lane_width=None,
                                      location=listing_loc)
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

                if code in listing_obj:
                    queryset_list = Listing.objects.filter(code=code)
                    if queryset_list.exists():
                        listing = queryset_list.first()
                        if listing.priority == 1 or listing.priority == 2:
                            if listing.user is None:
                                listing.user = new_listing.user
                            listing.realtor = new_listing.realtor
                            listing.status = new_listing.status
                            listing.reward_person = new_listing.reward_person
                            listing.reward_person_mobile = new_listing.reward_person_mobile
                            listing.extra_data = new_listing.extra_data
                            listing.location = new_listing.location
                            listing.is_published = new_listing.is_published
                            listing.save()
                            logger.info(f"row {line_count}: chỉ cập nhật {code} đã biên tập dữ liệu")
                        else:
                            listing.user = new_listing.user
                            listing.realtor = new_listing.realtor
                            listing.house_type = new_listing.house_type
                            listing.road_type = new_listing.road_type
                            listing.status = new_listing.status
                            listing.area = new_listing.area
                            listing.floors = new_listing.floors
                            listing.width = new_listing.width
                            listing.price = new_listing.price
                            listing.list_date = new_listing.list_date
                            listing.reward_person = new_listing.reward_person
                            listing.reward_person_mobile = new_listing.reward_person_mobile
                            listing.extra_data = new_listing.extra_data
                            listing.priority = new_listing.priority
                            listing.location = new_listing.location
                            listing.is_published = new_listing.is_published
                            listing.save()
                            logger.info(f"row {line_count}: update {code}")
                else:
                    queryset_list = Listing.objects.filter(address=new_listing.address,price=new_listing.price, district=new_listing.district, area=new_listing.area,
                                                           floors=new_listing.floors).order_by('-list_date')
                    if queryset_list.exists():
                        listing = queryset_list.first()
                        if listing.priority == 1 or listing.priority == 2:
                            if listing.user is None:
                                listing.user = new_listing.user
                            listing.realtor = new_listing.realtor
                            listing.status = new_listing.status
                            listing.is_published = new_listing.is_published
                            listing.save()
                            logger.info(
                                f"row {line_count}: cập nhật bđs đã có nhưng ko tìm thấy code {code} đã biên tập dữ liệu, từ trạng thái {listing.status} sang {new_listing.status}")
                        else:
                            listing.user = new_listing.user
                            listing.realtor = new_listing.realtor
                            listing.is_published = new_listing.is_published
                            listing.house_type = new_listing.house_type
                            listing.road_type = new_listing.road_type
                            listing.status = new_listing.status
                            listing.area = new_listing.area
                            listing.floors = new_listing.floors
                            listing.width = new_listing.width
                            listing.price = new_listing.price
                            listing.list_date = new_listing.list_date
                            listing.reward_person = new_listing.reward_person
                            listing.reward_person_mobile = new_listing.reward_person_mobile
                            listing.extra_data = new_listing.extra_data
                            listing.location = new_listing.location
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
