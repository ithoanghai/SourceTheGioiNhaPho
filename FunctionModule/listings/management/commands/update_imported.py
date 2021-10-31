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
                new_title = f'Bán {get_short_title_from_house_type(listing.house_type)} {listing.street} {listing.district_name()} '
                if listing.area >= 30:
                    new_title += f'{listing.area:.0f}m '
                if listing.floors and listing.floors > 1:
                    new_title += f'{listing.floors} tầng '
                new_title += f'{listing.display_price}'
                new_title = new_title.upper()
                new_desc = render_to_string('listings/defaultDescription.html', context={"listing": listing})
                listing.code = new_code
                listing.title = new_title
                listing.desc = new_desc
                listing.save()
        except Exception as ex:
            print(ex)
