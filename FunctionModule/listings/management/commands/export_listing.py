import csv

from django.core.management.base import BaseCommand

from FunctionModule.listings.export import prepare_fb_headers, prepare_fb_listing_data
from FunctionModule.listings.models import Listing


class Command(BaseCommand):
    help = "Export listings to csv"

    def handle(self, *args, **options):
        try:
            with open('test.csv', 'w') as fp:
                headers = prepare_fb_headers()
                writer = csv.DictWriter(fp, fieldnames=headers)
                writer.writeheader()
                for listing in Listing.objects.all():
                    listing_data = prepare_fb_listing_data(listing)
                    writer.writerow(listing_data)

        except Exception as ex:
            print(ex)
