from django.urls import reverse

from .choices import Status


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
        "image",
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


def prepare_fb_listing_data(listing):
    price = listing.sale_price or listing.price
    url = reverse('listing_detail', kwargs={'listing_id': listing.id})
    full_url = f'https://thegioinhaphovietnam.com.vn/{url}'
    main_photo_url = f'https://thegioinhaphovietnam.com.vn/{listing.main_photo.url}'
    listing_data = {
        "home_listing_id": listing.code,
        "name": listing.title,
        "description": listing.description,
        "availability": listing.get_status_display(),
        "price": f'{price:5.2f} tỷ VND',
        "home_listing_group_id": None,
        "ac_type": None,
        "agent_name": listing.realtor.user.name,
        "agent_company": "TGNP",
        "furnish_type": listing.furniture_design,
        "tenure_type": listing.get_registration_type_display(),
        "sale_type": listing.get_status_display() if listing.status == Status.SALE else None,
        "garden_type": None,
        "days_on_market": None,
        "url": full_url,
        "image": main_photo_url,
        "fee_schedule_url": None,
        "heating_type": None,
        "laundry_type": None,
        "listing_type": listing.get_house_type_display(),
        "agent_rera_id": None,
        "property_rera_id": None,
        "num_baths": listing.bathrooms if listing.bathrooms else None,
        "num_beds": listing.bedrooms,
        "num_rooms": listing.bedrooms,
        "num_units": None,
        "parking_type": listing.get_road_type_display(),
        "partner_verification": listing.is_verified,
        "pet_policy": None,
        "min_price": None,
        "max_price": None,
        "property_type": listing.get_house_type_display(),
        "area_size": listing.area,
        "built_up_area_size": listing.area_real or listing.area,
        "property_tax": None,
        "condo_fee": None,
        "coownership_charge": None,
        "parking_spaces": listing.get_road_type_display(),
        "area_unit": 'm2',
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
        "land_area_size": listing.area,
        "security_deposit": None,
        "holding_deposit": None,
        "application_fee": None,
        "pet_deposit": None,
        "pet_monthly_fee": None,
        "floor_types[0]": f'{listing.floors:2.0f} tầng',
        "unit_features[0]": listing.salient_features,
        "construction_status": listing.get_condition_display(),
        "coownership_num_lots": None,
        "coownership_status": None,
        "coownership_proceedings_status": None,
        "special_offers[0]": None,
        "pet_restrictions[0]": None,
        "building_amenities[0]": listing.living_facilities,
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