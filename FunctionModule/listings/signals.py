from django.db.models.signals import post_save
from django.dispatch import receiver

from TownhouseWorldRealestate.search_engine import listing_search
from TownhouseWorldRealestate.search_engine.search_client import suggestions_search
from .location_image import download_listing_location_image
from .models import Listing, ListingSerializer
from .search import prepare_index_from_listing


@receiver(post_save, sender=Listing)
def update_index(sender, instance: Listing, **kwargs):
    try:
        listing_search.update_documents([ListingSerializer(instance).data])
    except Exception as e:
        print(e)

    try:
        suggestions_data = prepare_index_from_listing(instance)
        suggestions_search.update_documents(suggestions_data)
    except Exception as e:
        print(e)

    try:
        created = kwargs.get('created', False)
        if created:
            download_listing_location_image(instance)
    except Exception as e:
        print(e)
