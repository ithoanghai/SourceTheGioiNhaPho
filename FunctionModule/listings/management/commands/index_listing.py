from django.core.management.base import BaseCommand

from FunctionModule.listings.models import Listing, ListingSerializer
from TownhouseWorldRealestate.search_engine import search_client


class Command(BaseCommand):
    help = "Create index for all listings for search"

    def handle(self, *args, **options):
        client = search_client
        client.create_index('listings', {'primaryKey': 'id'})
        listings = Listing.objects.all()
        docs = ListingSerializer(listings, many=True, )
        index = client.index('listings')
        index.update_searchable_attributes(['code', 'state_name', 'district_name', 'ward_name', 'street',
                                            'house_type', 'urban_area', 'road_type'])
        index.delete_all_documents()
        index.add_documents(docs.data)
