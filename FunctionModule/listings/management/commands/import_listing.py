from django.core.management.base import BaseCommand

from FunctionModule.listings.import_csv import handle_import, logger


class Command(BaseCommand):
    help = "Import listings from xlsx"

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)
        parser.add_argument('-t', '--type', type=str)

    def handle(self, *args, **kwargs):
        try:
            file_path = kwargs['file_path'][0]
            listing_type = kwargs.get('type') or 'K2'
            handle_import(file_path, listing_type)
        except Exception as ex:
            print(ex)
