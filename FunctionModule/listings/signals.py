from django.db.models.signals import post_save
from django.dispatch import receiver

from .location_image import download_listing_location_image
from .models import Listing, ListingSerializer
from .search_engine import listing_search


@receiver(post_save, sender=Listing)
def update_index(sender, instance: Listing, **kwargs):
    try:
        listing_search.update_documents([ListingSerializer(instance).data])
    except Exception as e:
        print(e)

    try:
        created = kwargs.get('created', False)
        if created:
            download_listing_location_image(instance)
    except Exception as e:
        print(e)
