from django.core.management.base import BaseCommand

from FunctionModule.listings.location_image import download_listing_location_image
from FunctionModule.listings.models import Listing, ListingSerializer


class Command(BaseCommand):
    help = "Download static location image for all listings"

    def handle(self, *args, **options):
        listings = Listing.objects.all()
        for l in listings:
            download_listing_location_image(l)
