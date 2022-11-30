import meilisearch

from TownhouseWorldRealestate import settings

_client = None


class SearchEngineClient(object):

    def __init__(self):
        global _client
        if not _client:
            _client = self._create_client()

    def _create_client(self):
        client = meilisearch.Client(f'http://{settings.MEILI_HOST}:{settings.MEILI_PORT}',settings.MEILI_MASTER_KEY)

        return client

    def get_client(self):
        global _client
        if not _client:
            _client = self._create_client()
        return _client


engine_client = SearchEngineClient()
search_client: meilisearch.Client = engine_client.get_client()
listing_search = search_client.index('listings')
suggestions_search = search_client.index('suggestions')
