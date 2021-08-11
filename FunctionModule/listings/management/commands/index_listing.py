from django.core.management.base import BaseCommand

from FunctionModule.listings.models import Listing, ListingSerializer
from TownhouseWorldRealestate.search_engine import search_client


class Command(BaseCommand):
    help = "Create index for all listings for search"

    def handle(self, *args, **options):
        client = search_client
        index = client.index('listings')
        index.update_searchable_attributes(
            ['code', 'state_name', 'district_name', 'ward_name', 'street', 'urban_area'])
        index.update_distinct_attribute('code')
        # Current version of meilisearch python (0.15.1) use wrong url
        index.config.paths.attributes_for_faceting = 'filterable-attributes'
        index.update_attributes_for_faceting(['price', 'area', 'bedrooms', 'bathrooms', 'status',
                                              'is_verified', 'is_exclusive', 'is_published', 'direction',
                                              'house_type', 'transaction_type'])
        # See docs.meilisearch.com/learn/core_concepts/relevancy.html#default-order
        index.update_ranking_rules(
            ["words", "proximity", "exactness", "attribute", "typo", "wordsPosition", "desc(list_date",
             "asc(price)"])
        index.delete_all_documents()
        listings = Listing.objects.all()
        docs = ListingSerializer(listings, many=True, )
        index.add_documents(docs.data)
