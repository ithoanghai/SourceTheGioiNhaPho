from django.core.management.base import BaseCommand

from FunctionModule.listings.models import Listing
from FunctionModule.listings.search import prepare_index_from_listing
from TownhouseWorldRealestate.search_engine import search_client


class Command(BaseCommand):
    help = "Create index for all listings for search"

    def handle(self, *args, **options):
        client = search_client
        # client.create_index('suggestions', {'primaryKey': 'id'})
        index = client.index('suggestions')
        index.update_searchable_attributes(['text'])
        index.delete_all_documents()

        suggestion_data = []

        for listing in Listing.objects.all():
            suggestion_data += prepare_index_from_listing(listing)

        index.add_documents(suggestion_data)
