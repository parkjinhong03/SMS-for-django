from typing import Mapping
from elasticsearch import Elasticsearch
from django.conf import settings
from _meta.singleton import Singleton


class ElasticsearchAgent(metaclass=Singleton):
    """elasticsearch agent class that do searching or inserting, etc ..."""
    client: Elasticsearch

    def __init__(self, client: Elasticsearch = None):
        if client is None:
            raise ValueError('must set elasticsearch_client')
        self.client = client

    def search(self, body: Mapping, index: str = settings.ELASTICSEARCH_INDEX):
        return self.client.search(index=index, body=body)
