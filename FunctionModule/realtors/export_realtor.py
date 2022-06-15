from django.urls import reverse

def prepare_export_realtor_data(realtor):
    #full_url = f'https://thegioinhaphovietnam.com.vn{url}'
    realtor_data = {
        # "home_listing_id": listing.code,  # Bắt buộc
        # "name": f'{listing.code}',  # Bắt buộc
        # "description": get_description(listing),  # Bắt buộc
        # "availability": get_availability(listing),  # Bắt buộc
        # "price": f'{price:5.2f} VND',  # Bắt buộc
        # "url": full_url,  # Bắt buộc | The URL of the specific page where people can view the listing.
        # "address.addr1": f'%s, %s' % (listing.district_name(), listing.state_name()),  # Bắt buộc
        # "address.city": f'%s' % (listing.state),  # Bắt buộc
        # "address.country": f'Việt Nam',  # Bắt buộc
        # "latitude": listing.lat,  # Bắt buộc
        # "longitude": listing.long,  # Bắt buộc
        # "neighborhood[0]": listing.residential_community,  # Bắt buộc
        # "image[0].url": main_photo_url,  # Bắt buộc
        # "image[0].tag[0]": main_photo_url,  # Bắt buộc
        #
        # "home_listing_group_id": None,
        # "custom_number_0": 1,
        # "ac_type": "central",
        # "agent_name": "Hoàng Hải",
        # "agent_company": "TGNP",
        # "furnish_type": get_furnish_type(listing),
        # "tenure_type": get_tenure_type(listing),
        # "sale_type": get_sale_type(listing),
        # "garden_type": None,
        # "days_on_market": None,
        # "fee_schedule_url": None,
        # "heating_type": "central",
        # "laundry_type": None,
        # "listing_type": get_listing_type(listing),
        # "agent_rera_id": None,
        # "property_rera_id": None,
        # "num_baths": listing.bathrooms if listing.bathrooms else None,
        # "num_beds": listing.bedrooms,
        # "num_rooms": None,
        # "num_units": None,
        # "parking_type": listing.parking_type,
        # "partner_verification": "verified" if listing.is_verified else 'none',
        # "pet_policy": None,
        # "min_price": None,
        # "max_price": None,
        # "property_type": get_property_type(listing),
        # "area_size": int(listing.area),
        # "built_up_area_size": int(real_size),
        # "property_tax": None,
        # "condo_fee": None,
        # "coownership_charge": None,
        # "parking_spaces": None,
        # "area_unit": None,  # Total area of unit; including outer walls; balcony.
        # "year_built": "2022",
        # "address.addr2": listing.ward_name(),
        # "address.addr3": listing.street,
        # "address.city_id": None,
        # "address.region": listing.state,
        # "address.postal_code": None,
        # "address.unit_number": None,
        # "energy_rating_eu.grade": None,
        # "energy_rating_eu.value": None,
        # "co2_emission_rating_eu.grade": None,
        # "co2_emission_rating_eu.value": None,
        # "additional_fees_description": None,
        # "num_pets_allowed": None,
        # "land_area_size": int(listing.area),
        # "security_deposit": None,
        # "holding_deposit": None,
        # "application_fee": None,
        # "pet_deposit": None,
        # "pet_monthly_fee": None,
        # "floor_types[0]": None,
        # "unit_features[0]": None,
        # "construction_status": None,
        # "coownership_num_lots": None,
        # "coownership_status": None,
        # "coownership_proceedings_status": None,
        # "special_offers[0]": None,
        # "pet_restrictions[0]": None,
        # "building_amenities[0]": None,
        # "broker_fee": None,
        # "first_month_rent": None,
        # "last_month_rent": None,
        # "utilities_included_in_rent[0]": None,
        # "rental_room_type": None,
        # "private_room_bathroom_type": None,
        # "number_of_co_renters": None,
        # "private_room_area_size": None,
        # "virtual_tour_url": None,
    }
    return realtor_data
