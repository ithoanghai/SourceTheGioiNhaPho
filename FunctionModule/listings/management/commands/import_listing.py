from django.core.management.base import BaseCommand

from FunctionModule.listings.import_csv import handle_import


class Command(BaseCommand):
    help = "Import listings from xlsx"

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            file_path = options['file_path'][0]
            handle_import(file_path)
        except Exception as ex:
            print(ex)
