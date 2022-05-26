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
from FunctionModule.cadastral.lookups import get_district_name
from FunctionModule.listings.helpers import print_trace, get_house_type_short, get_short_title_from_house_type
from FunctionModule.listings.models import Listing, Status, TransactionType, HouseType, RoadType, ListingHistory
from FunctionModule.realtors.models import Realtor

default_password = 'tgnpvn@2021'
logger = logging.getLogger(__name__)


def read_header(header_row, listing_type):
    if listing_type == 'K1':
        logger.info(f"listing_type {listing_type} Nha Pho VN")
        header_dict = {
            "tieude": 0,
            "mota": 1,
            "mota-dauchu": 2,
            "anh-nha": 3,
            "anh-so": 4,
            "tgian": 5,
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
            "dt": 20,
            "trm2": 21,
            "hientrang": 22,
            # "thanh-pho": 20,
            # "so-tang": 23,
            # "mat-tien": 23,
            # "hoa-hong": 23,
            # "nguon": 23,
        }
    elif listing_type == 'K2':
        logger.info(f"listing_type {listing_type} Thien Khoi")
        header_dict = {
            "tieude": 0,
            "mota": 1,
            "mota-dauchu": 2,
            "anh-nha": 3,
            "anh-so": 4,
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
            "pho": 21,
            "dac-diem": 21,
            "huong": 21,
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
                        rel = Realtor.objects.filter(user__phone=fone)
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
                road_type = RoadType.ALLEY_TRIBIKE
                direction = ""
                reward = 100
                bonus_rate = 3
                desc = ""
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
                name = row[header_dict['dau-chu']]
                realtor = Realtor.objects.filter(pk=1).first()

                #read state, district information
                try:
                    if listing_type=='K1':
                        state_name = 'Hà Nội'
                    else:
                        state_name = row[header_dict['thanh-pho']]
                    district = row[header_dict['quan']]
                    if not district:
                        logger.info(f"No district. Continue in line {line_count}")
                        continue
                    if district in hanoi_districts:
                        district_code = hanoi_districts[district]
                    else:
                        # logger.info(f"District code not found. Continue in line {line_count}")
                        continue
                except ValueError:
                    state_name = 'Hà Nội'
                    pass

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

                #Read information about area
                area = row[header_dict['dt']]
                try:
                    # area = float(row[header_dict['dt']].replace('c4', ''))
                    if not area or area == '#VALUE!':
                        continue
                    area = Decimal(area.replace(',', '.').replace(' ', ''))
                except ValueError:
                    logger.info(f"error area  {area}")
                    pass

                # Read information about floor
                try:
                    if listing_type != "K1":
                        floor = row[header_dict['so-tang']]
                    else:
                        floor = None
                    if floor is not None:
                        floor = Decimal(floor.replace(',', '.').replace(' ', ''))
                        if floor == 0:
                            house_type = HouseType.LAND
                        elif floor == 1:
                            house_type = HouseType.LOFT_HOUSE
                        else:
                            house_type = HouseType.TOWN_HOUSE
                except ValueError:
                    logger.info(f"error floor  {floor}")
                    pass

                # Read information about width
                try:
                    if listing_type != "K1":
                        width = row[header_dict['mat-tien']]
                    else:
                        width = None
                    if width is not None:
                        width = Decimal(width.replace(',', '.').replace(' ', ''))
                except ValueError:
                    logger.info(f"error width  {width}")
                    pass

                # Read real estate price information
                price = row[header_dict['gia']]
                try:
                    if price == '#VALUE!':
                        continue
                    price = price.split(' ')[0]
                    price = Decimal(price.replace(',', '.').replace(' ', ''))
                    if not price:
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
                        is_published = True
                    elif status == 'Đã bán' or status == 'Đã cọc':
                        status = Status.SOLD
                        is_published = False
                    elif status == 'Dừng bán' or status == 'Tạm dừng bán':
                        status = Status.STOP_SELLING
                        is_published = False
                    elif status == 'Hạ chào':
                        status = Status.SALE
                        is_published = True
                    else:
                        status = Status.SOLD
                        is_published = False
                    # 008 Q. Hoàng Mai,009 Q. Thanh Xuân, 020 H. Thanh Trì, 278 H. Thanh Oai, 268 Q. Hà Đông
                    if district_code == '008' or district_code == '009' or district_code == '020' or district_code == '278' or district_code == '268':
                        priority = 8
                    else:
                        priority = 9
                except ValueError:
                    logger.info(f"error status {status}")
                    pass

                #read đơn vị
                don_vi = row[header_dict['don-vi']]
                try:
                    if don_vi is None:
                        don_vi = "Thiên Khôi"
                except ValueError:
                    don_vi = "Thiên Khôi"

                #read nguồn & hoa hồng
                try:
                    if listing_type != 'K1':
                        nguon = row[header_dict['nguon']]
                        hoa_hong = row[header_dict['hoa-hong']]
                        extra_add = f' Nguồn {nguon}, hoa hồng {hoa_hong}.'
                    else:
                        hoa_hong = ''
                        extra_add = f' Nguồn nhà phố, hoa hồng 3%, xác minh lại với đầu chủ {name}.'
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
                except ValueError:
                    extra_add = f' Nguồn nhà phố, hoa hồng 3%, xác minh lại với đầu chủ {name}.'

                #Read information about specialist phone number. Add user from phone list
                phone = row[header_dict['sdt']]
                try:
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
                        extra_data = f'Liên hệ với {name}, {phone}, {don_vi} để giao dịch.\n{extra_add}'
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
                                    extra_data = f'Liên hệ với {name}, {extra_phone}, {don_vi} để giao dịch.\n' + extra_add
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

                # get address and street
                addr = row[header_dict['dia-chi']].replace('.', '/').replace(' , ', ', ').replace(',', '/').replace(
                    'Số ', '').replace(' ', ' ')
                street = row[header_dict['pho']]
                try:
                    so_nha = addr.split(' ')
                    deep_address = so_nha[0].split('/')
                    if "+" in deep_address:
                        deep_address = deep_address.split('+')
                    if len(street) > 0:
                        full_addr = f'{addr}, {street}, {district}, {state_name}'
                    else:
                        lensonha = int(len(so_nha[0]))
                        street = addr[lensonha:].replace('(', '').replace(')', '').replace('/', '').replace('  ', '')
                        street = street.translate(street.maketrans('', '', digits))
                        full_addr = f'{addr}, {district}, {state_name}'
                    full_addr = full_addr.replace(' TT ', ' tập thể ').replace('CCCC', 'Chung cư cao cấp').replace('CCMN', 'Chung cư mini').replace('CC ', 'Chung cư ')
                    add_search_map = f'{deep_address[0]} {street}, {district}, {state_name}'
                    add_search_map = add_search_map.replace('  ', ' ')
                except ValueError:
                    logger.info(f'error address {full_addr}')

                # search location on map
                try:
                    listing_loc = Point(105.83549388560711, 20.976795401917798)
                    if add_search_map in searched_locations:
                        if searched_locations[add_search_map]:
                            listing_loc = Point(searched_locations[add_search_map][0],
                                                searched_locations[add_search_map][1])
                    else:
                        #if api_key:
                        #geolocator = GeocodeEarth(api_key=api_key)
                        geolocator = Nominatim(user_agent="thegioinhaphovietnam.com.vn")
                        #GeocodeEarth.geocoders.options.default_user_agent = "my-application"
                        hanoi_bounds = ((21.097341, 105.929947), (20.920105, 105.702667))
                        location = geolocator.geocode(add_search_map, timeout=None, bounded=True, viewbox=hanoi_bounds)
                        if location and location.point:
                            listing_loc = Point(location.point.longitude, location.point.latitude)
                            searched_locations[add_search_map] = [location.point.longitude,
                                                             location.point.latitude]
                        else:
                            searched_locations[add_search_map] = None
                except ValueError:
                    logger.info(f"error search location {add_search_map}")

                #get đặc điểm bđs, title
                title_hot = ''
                desc = row[header_dict['dac-diem']].replace('N', 'n').replace('K', 'k').replace('B', 'b').replace('X', 'x').replace('D', 'd')\
                    .replace('M', 'm').replace('G', 'g').replace('Ô', 'ô').replace('T', 't').replace('G', 'g')\
                    .replace('Á', 'á').replace('Đ', 'đ').replace('P', 'p').replace('C', 'c')
                try:
                    if biet_thu in full_addr.lower():
                        house_type = HouseType.VILLA
                        road_type = RoadType.ALLEY_CAR_2
                    elif shop_house in full_addr.lower():
                        house_type = HouseType.SHOP_HOUSE
                        road_type = RoadType.ALLEY_CAR_2
                    elif lien_ke in full_addr.lower() or dich_vu in full_addr.lower() or lo in full_addr.lower() or du_an in full_addr.lower() or desc == 'Liền Kề' or thap_tang in full_addr.lower():
                        house_type = HouseType.PLOT
                        road_type = RoadType.ALLEY_CAR_2
                    elif "chung cư mini" in full_addr.lower():
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR
                    elif cao_tang in full_addr.lower() or chung_cu in full_addr.lower() or " tt " in full_addr.lower() or tap_the in full_addr.lower():
                        full_addr = full_addr.replace(' TT ', ' tập thể ').replace('CCCC', 'Chung cư cao cấp')
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR_2

                    if 'đất dự án' in desc:
                        house_type = HouseType.PLOT
                        road_type = RoadType.ALLEY_CAR_2
                        trans_type = TransactionType.PROJECT
                    elif 'chung cư' in desc:
                        house_type = HouseType.APARTMENT
                        road_type = RoadType.ALLEY_CAR_2
                    elif 'ngõ ô tô' in desc:
                        house_type = HouseType.TOWN_HOUSE
                        road_type = RoadType.ALLEY_CAR
                        title_hot = 'ngõ ô tô'
                    elif 'ngõ 3 gác' in desc:
                        house_type = HouseType.TOWN_HOUSE
                        road_type = RoadType.ALLEY_TRIBIKE
                    elif 'ngõ xe máy' in desc:
                        house_type = HouseType.TOWN_HOUSE
                        road_type = RoadType.ALLEY_BIKE
                    elif 'kinh doanh' in desc:
                        road_type = RoadType.ALLEY_CAR
                        title_hot = 'kinh doanh tốt'

                    if (len(deep_address) == 1 and deep_address[0].isalnum()) or ('mặt phố' in desc):
                        house_type = HouseType.STREET_HOUSE
                        road_type = RoadType.ALLEY_CAR_2

                    if len(desc) > 0:
                        extra_data = f'Bất động sản {desc}. {full_addr}.\n' + extra_data
                except ValueError:
                    logger.info(f"error dac-diem {desc}")

                # Phân tích cú pháp thông số để lấy diện tích, số tầng, mặt tiền từ file nguồn nhà phố
                if listing_type == "K1":
                    encoded_num = row[header_dict['thong-so']].replace('  ', ' ')
                    splitter = encoded_num.split(' ')
                    floor = 0
                    try:
                        floor_code = splitter[1]
                        floor_code = slugify(floor_code.lower().replace('đ', 'd').replace('ấ', 'a').replace('t', '')
                                    .replace('c4', 'c').replace(' ', ''))
                        if floor_code == 'c' or floor_code == 'cap':
                            floor = 1
                            house_type = HouseType.LOFT_HOUSE
                        elif floor_code == 'da' or floor_code == 'd':
                            floor = 0
                            house_type = HouseType.LAND
                        else:
                            floor = int(floor_code)

                        splitter_len = len(splitter)
                        if splitter_len == 4 or splitter_len == 3:
                            width = splitter[2].replace(',', '.').replace(' ', '').split('/')
                            width = Decimal(width[0].replace(',', '.').replace(' ', ''))
                        else:
                            width = None

                    except ValueError:
                        logger.info(f"Cannot decode encoded_num {encoded_num}. Continue in line {line_count}")

                title = f'Bán {get_short_title_from_house_type(house_type)} {title_hot} {street} {get_district_name(district_code)} '
                if area >= 30:
                    title += f'{area:.0f}m '
                if house_type == HouseType.APARTMENT or house_type == HouseType.CONDO_TEL or house_type == HouseType.SERVICE_APARTMENT or house_type == HouseType.PENT_HOUSE:
                    title += f'tầng {floor:.0f} giá '
                elif int(floor) > 3:
                    title += f'{floor:.0f} tầng'
                if price % 1 == 0:
                    title += f'{price:.0f} tỷ'
                else:
                    title += f'{price:.1f} tỷ'
                title = title.upper().replace('  ', ' ')
                starter = get_house_type_short(house_type)
                if width is not None:
                    code = f'{starter}{created.strftime("%y%m")}{listing_type}{district_code}{int(area)}{int(floor)}{width}{price}'
                else:
                    code = f'{starter}{created.strftime("%y%m")}{listing_type}{district_code}{int(area)}{int(floor)}{price}'

                new_listing = Listing(user=user, realtor=user.realtor, code=code, status=status, title=title,
                                      street=street, address=full_addr, area=area, transaction_type=trans_type,
                                      house_type=house_type, road_type=road_type, list_date=created,
                                      direction=direction, price=price, reward_person=realtor.user.name, priority=priority,
                                      reward_person_mobile=realtor.user.phone, reward=reward, bonus_rate=bonus_rate,
                                      extra_data=extra_data, state=state_code, district=district_code, is_published=is_published,
                                      width=width, floors=floor, average_price=price_per_area, length=None, lane_width=None,
                                      location=listing_loc)
                new_listing.description = render_to_string('listings/defaultDescription.html',
                                               context={"listing": new_listing, "desc": desc}).replace('  ', ' ')

                query = (Q(address__contains=so_nha[0]) & Q(area=area) & Q(floors=floor) & Q(width=width) & Q(price=price))| \
                        (Q(address__contains=so_nha[0]) & Q(area=area) & Q(street=street) & Q(state=state_code) & Q(district=district_code))
                querylist_list = Listing.objects.filter(Q(code=code) | Q(address=full_addr) | query).order_by('-list_date')
                #Nếu kho đã tồn tại bđs
                if querylist_list.exists():
                    count_update = 0
                    listing_fisrt = None
                    if querylist_list.count() > 1:
                        print(f"row {line_count}: kho đang có {querylist_list.count()} bđs: {new_listing}")
                    # duyệt toàn bộ tìm các listing trùng lặp đang có trong kho
                    for listing in querylist_list:
                        logger.info(f"row {line_count}: listing {listing}, count_update {count_update}")
                        #Kiểm tra listing tiếp theo, nếu cũ hơn thì xóa, mới hơn thì cập nhật
                        if listing_fisrt is None:
                            listing_fisrt = Listing.objects.get(id=listing.id)

                        # nếu listing mới import cũ hơn listing trong kho thì chỉ đẩy listing này sang bảng listing history
                        if listing.list_date >= new_listing.list_date:
                            querylist_listhistory = ListingHistory.objects.filter(listing=listing_fisrt, list_date=new_listing.list_date)
                            #Kiểm tra trong listing history đã có trùng lặp chưa, nếu chưa có thì đẩy vào, nếu có rồi bỏ qua
                            if not querylist_listhistory.exists() and count_update >= 1:
                                new_listhis = ListingHistory.objects.create(listing=listing_fisrt, user=new_listing.user,
                                              realtor=new_listing.realtor, area=new_listing.area, floors=new_listing.floors, width=new_listing.width,
                                              bathrooms=new_listing.bathrooms, bedrooms=new_listing.bedrooms, price=new_listing.price, reward_person_mobile=new_listing.reward_person_mobile,
                                              reward_person=new_listing.reward_person, extra_data=new_listing.extra_data,
                                              warehouse=listing_type, list_date=new_listing.list_date)
                                new_listhis.save()
                                logger.info(f"row {line_count}: tạo mới lịch sử bđs {new_listhis} từ listing import cũ hơn {new_listing}, bđs gốc {listing_fisrt}")

                        #Nếu listing đưa vào là mới nhất là lần đầu thì cập nhật thông tin mới cho listing
                        elif listing.list_date < new_listing.list_date:
                            querylist_listhistory = ListingHistory.objects.filter(listing=listing_fisrt, list_date=listing.list_date)
                            # Kiểm tra trong listing history đã có trùng lặp chưa, nếu chưa có thì đẩy vào, nếu có rồi bỏ qua
                            if not querylist_listhistory.exists() and count_update >= 1:
                                #Đẩy thông tin listing cũ vào lịch sử listing
                                new_listhis = ListingHistory.objects.create(listing=listing_fisrt, user=listing.user,
                                              realtor=listing.realtor, area=listing.area, floors=listing.floors, width=listing.width,
                                              bathrooms=listing.bathrooms, bedrooms=listing.bedrooms, price=listing.price, reward_person_mobile=listing.reward_person_mobile,
                                              reward_person=listing.reward_person, extra_data=listing.extra_data, warehouse=listing_type, list_date=listing.list_date)
                                new_listhis.save()
                                logger.info(f"row {line_count}: Đẩy thông tin listing {listing} cũ hơn trên server vào lịch sử listing {new_listhis}")
                            #Cập nhật thông tin mới nhất cho listing đang có
                            if listing.priority == 1 or listing.priority == 2:
                                if listing_fisrt.user is None:
                                    listing_fisrt.user = new_listing.user
                                listing_fisrt.realtor = new_listing.realtor
                                listing_fisrt.status = new_listing.status
                                listing_fisrt.street = new_listing.street
                                listing_fisrt.address = new_listing.address
                                listing_fisrt.location = new_listing.location
                                listing_fisrt.code = new_listing.code
                                listing_fisrt.house_type = new_listing.house_type
                                listing_fisrt.road_type = new_listing.road_type
                                listing_fisrt.reward_person = new_listing.reward_person
                                listing_fisrt.reward_person_mobile = new_listing.reward_person_mobile
                                listing_fisrt.extra_data = new_listing.extra_data
                                listing_fisrt.list_date = new_listing.list_date
                                listing_fisrt.is_published = new_listing.is_published
                                listing_fisrt.save()
                                logger.info(f"row {line_count}: cập nhật {listing} prior {listing.priority} từ {new_listing}")
                            else:
                                listing_fisrt.user = new_listing.user
                                listing_fisrt.realtor = new_listing.realtor
                                listing_fisrt.house_type = new_listing.house_type
                                listing_fisrt.road_type = new_listing.road_type
                                listing_fisrt.status = new_listing.status
                                listing_fisrt.area = new_listing.area
                                listing_fisrt.floors = new_listing.floors
                                listing_fisrt.width = new_listing.width
                                listing_fisrt.price = new_listing.price
                                listing_fisrt.title = new_listing.title
                                listing_fisrt.description = new_listing.description
                                listing_fisrt.reward_person = new_listing.reward_person
                                listing_fisrt.reward_person_mobile = new_listing.reward_person_mobile
                                listing_fisrt.extra_data = new_listing.extra_data
                                listing_fisrt.priority = new_listing.priority
                                listing_fisrt.street = new_listing.street
                                listing_fisrt.address = new_listing.address
                                listing_fisrt.location = new_listing.location
                                listing_fisrt.code = new_listing.code
                                listing_fisrt.status = new_listing.status
                                listing_fisrt.list_date = new_listing.list_date
                                listing_fisrt.is_published = new_listing.is_published
                                listing_fisrt.save()
                                logger.info(f"row {line_count}: cập nhật {listing} prior {listing.priority} từ {new_listing}")
                        if count_update >= 1 and listing.id is not None:
                            findlisthistory = ListingHistory.objects.filter(listing=listing)
                            if findlisthistory.exists():
                                for hislist in findlisthistory:
                                    hislist.listing = listing_fisrt
                                    hislist.save()
                            else:
                                listing.delete()
                            print(f"row {line_count}: xóa listing thừa: {listing}")

                        count_update += 1
                else:
                    new_listing.save()
                    print(f"row {line_count}: tạo mới listing: {new_listing} chưa có")

    except Exception as ex:
        print(f"Error occurred at line: {line_count} type {type(ex)}")
        print_trace(ex)
    finally:
        print(f'Read {line_count} lines')
        with open('saved_search.json', 'w', encoding='utf-8') as f:
            json.dump(searched_locations, f, ensure_ascii=False)
