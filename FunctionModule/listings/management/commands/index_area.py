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
        # Current version of meilisearch python (0.15.1) use wrong url
        #index.config.paths.attributes_for_faceting = 'filterable-attributes'
        #index.update_attributes_for_faceting(['text'])
        # See docs.meilisearch.com/learn/core_concepts/relevancy.html#default-order
        #index.update_ranking_rules(
        #    ["words", "proximity", "exactness", "attribute", "typo", "wordsPosition"])
        index.delete_all_documents()

        suggestion_data = []

        for listing in Listing.objects.all():
            suggestion_data += prepare_index_from_listing(listing)

        index.add_documents(suggestion_data)
