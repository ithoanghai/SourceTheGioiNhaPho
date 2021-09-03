from django.urls import reverse

from .choices import Status, RoadType, Condition, HouseType, FurnishType, RegistrationType


def prepare_fb_headers():
    return [
        "home_listing_id",
        "name",
        "description",
        "availability",
        "price",
        "home_listing_group_id",
        "ac_type",
        "agent_name",
        "agent_company",
        "furnish_type",
        "tenure_type",
        "sale_type",
        "garden_type",
        "days_on_market",
        "url",
        "image[0].url",
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
        "parking_type",
        "parking_spaces",
        "area_unit",
        "year_built",
        "address.addr1",
        "address.addr2",
        "address.addr3",
        "address.city",
        "address.city_id",
        "address.region",
        "address.postal_code",
        "address.country",
        "address.unit_number",
        "latitude",
        "longitude",
        "neighborhood[0]",
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
      # "floor_types[0]",
      #  "unit_features[0]",
        "construction_status",
        "coownership_num_lots",
        "coownership_status",
        "coownership_proceedings_status",
        "special_offers[0]",
        "pet_restrictions[0]",
      #  "building_amenities[0]",
        "broker_fee",
        "first_month_rent",
        "last_month_rent",
        "utilities_included_in_rent[0]",
        "rental_room_type",
        "private_room_bathroom_type",
        "number_of_co_renters",
        "private_room_area_size",
        "virtual_tour_url",
        "applink.android_app_name",
        "applink.android_package",
        "applink.android_url",
        "applink.ios_app_name",
        "applink.ios_app_store_id",
        "applink.ios_url",
        "applink.ipad_app_name",
        "applink.ipad_app_store_id",
        "applink.ipad_url",
        "applink.iphone_app_name",
        "applink.iphone_app_store_id",
        "applink.iphone_url",
        "applink.windows_phone_app_id",
        "applink.windows_phone_app_name",
        "applink.windows_phone_url",
    ]

ONE_BILLION = 1000000000


def get_parking_type(road_type):
    if road_type == RoadType.ALLEY_CAR_2:
        return 'off_street'
    elif road_type == RoadType.ALLEY_CAR_TRIBIKE:
        return 'street'
    else:
        return 'none'


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


  # return value in  "apartment", "apartment_room", "builder_floor", "bungalow", "condo", "condo_room",
# "house", "house_in_condominium", "house_in_villa", "house_room", "land", "loft", "manufactured", "other", "other_room",
# "penthouse", "single_family_home", "studio", "townhouse", "townhouse_room"
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
        if listing.registration_type == RegistrationType.RED_BOOK:
            return 'strata_title'
        elif listing.registration_type == RegistrationType.PINK_BOOK:
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


def prepare_fb_listing_data(listing):
    price = listing.sale_price or listing.price
    url = reverse('listing_detail', kwargs={'listing_id': listing.id})
    full_url = f'https://thegioinhaphovietnam.com.vn/{url}'
    main_photo_url = f'https://thegioinhaphovietnam.com.vn{listing.main_photo.url}'
    real_size = listing.area_real or listing.area
    listing_data = {
        "home_listing_id": listing.code,
        "name": listing.title,
        "description": listing.description,
        "availability": get_status(listing.status),
        "price": f'{price:5.2f}',
        "home_listing_group_id": None,
        "ac_type": None,
        "agent_name": listing.realtor.user.name,
        "agent_company": "TGNP",
        "furnish_type": get_furnish_type(listing),
        "tenure_type": get_tenure_type(listing),
        "sale_type": get_sale_type(listing),
        "garden_type": None,
        "days_on_market": None,
        "url": full_url,
        "image[0].url": main_photo_url,
        "fee_schedule_url": None,
        "heating_type": None,
        "laundry_type": None,
        "listing_type": get_listing_type(listing),
        "agent_rera_id": None,
        "property_rera_id": None,
        "num_baths": listing.bathrooms if listing.bathrooms else None,
        "num_beds": listing.bedrooms,
        "num_rooms": listing.bedrooms,
        "num_units": None,
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
        "parking_type": listing.parking_type,
        "parking_spaces": get_parking_spaces(listing),
        "area_unit": 'sq_m',
        "year_built": None,
        "address.addr1": listing.district_name(),
        "address.addr2": listing.ward_name(),
        "address.addr3": listing.street,
        "address.city": listing.state_name(),
        "address.city_id": listing.state,
        "address.region": listing.state,
        "address.postal_code": None,
        "address.country": "Việt Nam",
        "address.unit_number": listing.address,
        "latitude": listing.lat,
        "longitude": listing.long,
        "neighborhood[0]": listing.residential_community,
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
       # "floor_types": None,
       # "unit_features": None,
        "construction_status": listing.construction,
        "coownership_num_lots": None,
        "coownership_status": None,
        "coownership_proceedings_status": None,
        "special_offers[0]": None,
        "pet_restrictions[0]": None,
      #  "building_amenities": listing.living_facilities,
        "broker_fee": None,
        "first_month_rent": None,
        "last_month_rent": None,
        "utilities_included_in_rent[0]": None,
        "rental_room_type": None,
        "private_room_bathroom_type": None,
        "number_of_co_renters": None,
        "private_room_area_size": None,
        "virtual_tour_url": None,
        "applink.android_app_name": None,
        "applink.android_package": None,
        "applink.android_url": None,
        "applink.ios_app_name": None,
        "applink.ios_app_store_id": None,
        "applink.ios_url": None,
        "applink.ipad_app_name": None,
        "applink.ipad_app_store_id": None,
        "applink.ipad_url": None,
        "applink.iphone_app_name": None,
        "applink.iphone_app_store_id": None,
        "applink.iphone_url": None,
        "applink.windows_phone_app_id": None,
        "applink.windows_phone_app_name": None,
        "applink.windows_phone_url": None,
    }
    return listing_data
