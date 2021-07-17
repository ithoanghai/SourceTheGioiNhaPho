import os
from pathlib import Path

import requests
from django.conf import settings

from FunctionModule.listings.models import Listing

API_URL = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static'


def get_listing_media_storage(listing_id):
    path = os.path.join(settings.MEDIA_ROOT, f'photos/listings/{listing_id}')
    return path


def prepare_request(lat, long):
    lat = round(lat, 4)
    long = round(long, 4)
    marker = f'pin-s+555555({long},{lat})'
    # long, lat, zoom, rotate
    map_details = f'{long},{lat},14.5,0'
    size = '715x550'
    url = f'{API_URL}/{marker}/{map_details}/{size}?access_token={settings.MAPBOX_API_KEY}'
    return url.strip(' ')


def download_listing_location_image(listing: Listing):
    url = prepare_request(listing.lat, listing.long)
    request = requests.get(url, timeout=8)
    if request.status_code == 200:
        path = get_listing_media_storage(listing.id)
        Path(path + '/locations').mkdir(parents=True, exist_ok=True)
        with open(path + '/locations/static.png', 'wb') as fh:
            fh.write(request.content)
            # request.raw.decode_content = True
            # shutil.copyfileobj(request.raw, fh)
