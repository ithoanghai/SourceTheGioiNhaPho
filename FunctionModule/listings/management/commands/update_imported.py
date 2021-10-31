from datetime import datetime

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from FunctionModule.listings import get_short_title_from_house_type, get_house_type_short
from FunctionModule.listings.models import Listing


class Command(BaseCommand):
    help = "Import listings from csv"

    def add_arguments(self, parser):
        parser.add_argument('id', type=str)
        parser.add_argument('-t', '--type', type=str)

    def handle(self, *args, **kwargs):
        try:
            l_id = kwargs['id']
            listing_type = kwargs.get('type') or 'K2'
            listings = Listing.objects.filter(id__gte=l_id)
            for listing in listings:  # Listing
                starter = get_house_type_short(listing.house_type)
                created_date = listing.list_date.strftime('%y%m')
                new_code = f'{starter}{created_date}{listing_type}{listing.id:05}'
                listing.code = new_code
                listing.save()
        except Exception as ex:
            print(ex)
