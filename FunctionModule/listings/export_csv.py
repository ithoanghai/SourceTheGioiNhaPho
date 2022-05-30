from django.urls import reverse

from .choices import Status, RoadType, Condition, HouseType, FurnishType, RegistrationType


ONE_BILLION = 1000000000


def get_parking_type(road_type):
    if road_type == RoadType.ALLEY_CAR_2:
        return 'off_street'
    elif road_type == RoadType.ALLEY_CAR_TRIBIKE:
        return 'street'
    else:
        return 'none'


def get_availability(listing):
    if listing.status == Status.SELLING:
        return 'available_soon'
    elif listing.status == Status.SALE:
        return 'off_market'
    elif listing.status == Status.STOP_SELLING:
        return 'sale_pending'
    elif listing.status == Status.SOLD:
        return 'recently_sold'


def get_visibility(listing):
    if listing.is_published == True:
        return 'published'
    else:
        return 'hidden'


 # return value  new, refurbished, used
def get_condition(listing):
    if listing.condition == Condition.NEW:
        return 'new'
    elif listing.condition == Condition.OLD:
        return 'used'
    else:
        return'refurbished'


def get_status(status):
    if status == Status.SELLING:
        return 'for_sale'
    elif status == Status.SALE:
        return 'for_sale'
    elif status == Status.SOLD:
        return 'recently_sold'
    else:
        return 'off_market'


def get_listing_type(listing):
    if listing.condition == Condition.NEW:
        return 'new_construction'
    else:
        return 'for_sale_by_owner'


 # return value  "new", "resale", "former"
def get_sale_type(listing):
    if listing.status == Status.SELLING:
        return 'new'
    elif listing.status == Status.SALE:
        return 'resale'
    else:
        return'former'


def get_property_type(listing):
    if listing.house_type == HouseType.STREET_HOUSE or listing.house_type == HouseType.LOFT_HOUSE or listing.house_type == HouseType.SHOP_HOUSE:
        return 'house'
    elif listing.house_type == HouseType.TOWN_HOUSE:
        return 'townhouse'
    elif listing.house_type == HouseType.APARTMENT or listing.house_type == HouseType.SERVICE_APARTMENT or listing.house_type == HouseType.OFFICE_TEL or listing.house_type == HouseType.OFFICE:
        return 'apartment'
    elif listing.status == HouseType.PENT_HOUSE:
        return 'penthouse'
    elif listing.house_type == HouseType.CONDO_TEL or listing.house_type == HouseType.BUILDING or listing.house_type == HouseType.BUILDING_BUSINESS:
        return 'condo'
    elif listing.house_type == HouseType.VILLA or listing.house_type == HouseType.VILLA_REST:
        return 'house_in_villa'
    elif listing.house_type == HouseType.LAND or listing.house_type == HouseType.LAND_BUSINESS or listing.house_type == HouseType.PLOT or listing.house_type == HouseType.PLOT or listing.house_type == HouseType.INDUSTRIAL_LAND:
        return 'land'
    elif listing.house_type == HouseType.WAREHOUSE_WORKSHOP:
        return 'manufactured'
    else:
        return'other'


    #"furnished", "semi-furnished", "unfurnished"
def get_furnish_type(listing):
    if listing.furnish_type == FurnishType.FURNISHED:
        return 'furnished'
    elif listing.furnish_type == FurnishType.SEMI_FURNISHED:
        return 'semi-furnished'
    else:
        return 'unfurnished'


    # "freehold", "leasehold", "strata_title", "cooperative", "power_of_attorney", "other",
    # "indonesia_hak_guna_banguan", "indonesia_hak_pakai", "indonesia_girik"
def get_tenure_type(listing):
        if listing.registration_type == RegistrationType.RED_PINK_BOOK or RegistrationType.VALID_DOCUMENTS:
            return 'strata_title'
        elif listing.registration_type == RegistrationType.BUSINESS_LICENSE or RegistrationType.CONSTRUCTION_LICENSE:
            return 'leasehold'
        elif listing.registration_type == RegistrationType.DONT_BOOK:
            return 'cooperative'
        else:
            return 'other'


# Các giá trị được công nhận cho những trường thông tin này bao gồm "garage", "none", "off_street", "other", "street"
def get_parking_type(listing):
    if listing.parking_type == RoadType.ALLEY_CAR_2 or listing.road_type == RoadType.ALLEY_CAR:
        return '1'
    else:
        return '0'


def get_parking_spaces(listing):
    if listing.road_type == RoadType.ALLEY_CAR_2 or listing.road_type == RoadType.ALLEY_CAR:
        return '1'
    else:
        return '0'


def get_additional_image_link_data(photos):
    list = ""
    for index, photo in enumerate(photos):
        list = list.__add__(f'https://thegioinhaphovietnam.com.vn{photo.url},')
    return list


def get_video_link(listing):
    link_main = ""
    for video in listing.videos:
        link_main = link_main.__add__(f'<a href="{video.video}">{video.video}</a>,')
    return link_main


def get_main_photo_url(listing):
    main_photo_url = listing.main_photo
    if main_photo_url is None:
        photo_url = f'https://thegioinhaphovietnam.com.vn/static/img/default_house_type/{listing.house_type}.jpg'
    else:
        photo_url = main_photo_url.url
    return photo_url


def get_description(listing):
    description = f'<div><p><bold> Mã BĐS: %s </bold></p> </div> ' \
                  f'<p> %s </p> <br>' \
                  % (listing.code, listing.description)
    if listing.furniture_design is not None:
        description = description + '<br> <p> %s </p>' + listing.furniture_design
    if listing.living_facilities is not None:
        description = description + '<br> <p> %s </p>' + listing.living_facilities
    if listing.location_advantage is not None:
        description = description + '<br> <p> %s </p>' + listing.location_advantage
    if listing.residential_community is not None:
        description = description + '<br> <p> %s </p>' + listing.residential_community
    if listing.regional_welfare is not None:
        description = description + '<br> <p> %s </p>' + listing.regional_welfare
    if listing.salient_features is not None:
        description = description + '<br> <p> %s </p>' + listing.salient_features
    if get_video_link(listing) != "":
        description = description + '<p> Để xem video BĐS này, bạn truy cập Link Video Youtube sau %s </p> </br>' % (get_video_link(listing))
    description1 = f'<p>Liên hệ ngay Thế giới Nhà Phố để được tư vấn, xem bđs</p>' \
                  f'<p>------------o0o--------------</p>' \
                  f'<p>BẤT ĐỘNG SẢN THẾ GIỚI NHÀ PHỐ</p>' \
                  f'<p>- Hàng chục nghìn sản phẩm BĐS, cam kết thông tin thật, chính xác 100%, không có thông tin ảo</p>' \
                  f'<p>- Tìm kiếm BĐS dễ dàng tại website của TGNP: https://Thegioinhaphovietnam.com.vn</p>' \
                  f'<p>- Hotline: 0916.286.256 - 0971.841.941 - 09.6439.9436 (Call/Zalo/Facebook)</p>' \
                  f'<p>- <a href= "https://www.facebook.com/TheGioiNhaPhoVietNam">Cửa hàng Facebook.com/TheGioiNhaPhoVietNam</a> </p>' \
                  f'<p>- <a href= "https://www.facebook.com/groups/khohang.thegioinhaphovietnam">Kho hàng Facebook.com/groups/khohang.thegioinhaphovietnam</a> </p>' \
                  f'<p>- <a href= "https://www.youtube.com/channel/UCiW13E8_8AHnHGiJGeZliug">Kênh Youtube KHO HÀNG THẾ GIỚI NHÀ PHỐ</a> </p>'
    return description + description1


def prepare_fb_headers():
    return [
        "home_listing_id",  # Bắt buộc
        "name",  # Bắt buộc
        "description",
        "availability",  # Bắt buộc
        "price",                     #Bắt buộc | The cost and currency of the home listing. The price is a number followed by the currency code (ISO 4217 standards)
        "url",  # Bắt buộc | The URL of the specific page where people can view the listing.
        "address.addr1",  # Bắt buộc
        "address.city",  # Bắt buộc
        "address.country",  # Bắt buộc
        "latitude",  # Bắt buộc
        "longitude",  # Bắt buộc
        "neighborhood[0]",  # Bắt buộc
        "image[0].url",  # Bắt buộc
        "image[0].tag[0]",  # Bắt buộc

        "home_listing_group_id",
        "custom_number_0",
        "ac_type",
        "agent_name",
        "agent_company",
        "furnish_type",
        "tenure_type",
        "sale_type",
        "garden_type",
        "days_on_market",
        "fee_schedule_url",
        "heating_type",
        "laundry_type",
        "listing_type",
        "agent_rera_id",
        "property_rera_id",
        "num_baths",
        "num_beds",
        "num_rooms",
        "num_units",
        "parking_type",
        "partner_verification",
        "pet_policy",
        "min_price",
        "max_price",
        "property_type",
        "area_size",
        "built_up_area_size",
        "property_tax",
        "condo_fee",
        "coownership_charge",
        "parking_spaces",
        "area_unit",
        "year_built",
        "address.addr2",
        "address.addr3",
        "address.city_id",
        "address.region",
        "address.postal_code",
        "address.unit_number",
        "energy_rating_eu.grade",
        "energy_rating_eu.value",
        "co2_emission_rating_eu.grade",
        "co2_emission_rating_eu.value",
        "additional_fees_description",
        "num_pets_allowed",
        "land_area_size",
        "security_deposit",
        "holding_deposit",
        "application_fee",
        "pet_deposit",
        "pet_monthly_fee",
        "floor_types[0]",
        "unit_features[0]",
        "construction_status",
        "coownership_num_lots",
        "coownership_status",
        "coownership_proceedings_status",
        "special_offers[0]",
        "pet_restrictions[0]",
        "building_amenities[0]",
        "broker_fee",
        "first_month_rent",
        "last_month_rent",
        "utilities_included_in_rent[0]",
        "rental_room_type",
        "private_room_bathroom_type",
        "number_of_co_renters",
        "private_room_area_size",
        "virtual_tour_url",

        "visibility",
        "condition",
        "image_link",
        "additional_image_link",
    ]


def prepare_fb_listing_data(listing):
    price = listing.sale_price or listing.price
    url = reverse('listing_detail', kwargs={'listing_id': listing.id})
    full_url = f'https://thegioinhaphovietnam.com.vn{url}'
    main_photo_url = get_main_photo_url(listing)
    real_size = listing.area_real or listing.area
    listing_data = {
        "home_listing_id": listing.code, # Bắt buộc
        "name": f'{listing.code}', # Bắt buộc
        "description": get_description(listing), # Bắt buộc
        "availability": get_availability(listing), # Bắt buộc
        "price": f'{price:5.2f} VND', # Bắt buộc
        "url": full_url, # Bắt buộc | The URL of the specific page where people can view the listing.
        "address.addr1": f'%s, %s' % (listing.district_name(), listing.state_name()), # Bắt buộc
        "address.city": f'%s' % (listing.state), # Bắt buộc
        "address.country": f'Việt Nam', # Bắt buộc
        "latitude": listing.lat, # Bắt buộc
        "longitude": listing.long, # Bắt buộc
        "neighborhood[0]": listing.residential_community,  # Bắt buộc
        "image[0].url": main_photo_url,  # Bắt buộc
        "image[0].tag[0]": main_photo_url,  # Bắt buộc

        "home_listing_group_id": None,
        "custom_number_0":  1,
        "ac_type": "central",
        "agent_name": "Hoàng Hải",
        "agent_company": "TGNP",
        "furnish_type": get_furnish_type(listing),
        "tenure_type": get_tenure_type(listing),
        "sale_type": get_sale_type(listing),
        "garden_type": None,
        "days_on_market": None,
        "fee_schedule_url": None,
        "heating_type": "central",
        "laundry_type": None,
        "listing_type": get_listing_type(listing),
        "agent_rera_id": None,
        "property_rera_id": None,
        "num_baths": listing.bathrooms if listing.bathrooms else None,
        "num_beds": listing.bedrooms,
        "num_rooms": None,
        "num_units": None,
        "parking_type": listing.parking_type,
        "partner_verification": "verified" if listing.is_verified else 'none',
        "pet_policy": None,
        "min_price": None,
        "max_price": None,
        "property_type": get_property_type(listing),
        "area_size": int(listing.area),
        "built_up_area_size": int(real_size),
        "property_tax": None,
        "condo_fee": None,
        "coownership_charge": None,
        "parking_spaces": None,
        "area_unit": None,  # Total area of unit; including outer walls; balcony.
        "year_built": "2022",
        "address.addr2": listing.ward_name(),
        "address.addr3": listing.street,
        "address.city_id": None,
        "address.region": listing.state,
        "address.postal_code": None,
        "address.unit_number": None,
        "energy_rating_eu.grade": None,
        "energy_rating_eu.value": None,
        "co2_emission_rating_eu.grade": None,
        "co2_emission_rating_eu.value": None,
        "additional_fees_description": None,
        "num_pets_allowed": None,
        "land_area_size": int(listing.area),
        "security_deposit": None,
        "holding_deposit": None,
        "application_fee": None,
        "pet_deposit": None,
        "pet_monthly_fee": None,
        "floor_types[0]": None,
        "unit_features[0]": None,
        "construction_status": None,
        "coownership_num_lots": None,
        "coownership_status": None,
        "coownership_proceedings_status": None,
        "special_offers[0]": None,
        "pet_restrictions[0]": None,
        "building_amenities[0]": None,
        "broker_fee": None,
        "first_month_rent": None,
        "last_month_rent": None,
        "utilities_included_in_rent[0]": None,
        "rental_room_type": None,
        "private_room_bathroom_type": None,
        "number_of_co_renters": None,
        "private_room_area_size": None,
        "virtual_tour_url": None,

        "visibility": get_visibility(listing),
        "condition": get_condition(listing),
        "additional_image_link": get_additional_image_link_data(listing.photos),
    }
    return listing_data
