from django.urls import path
from django.conf import settings
from elasticsearch import Elasticsearch

from . import views
from codec.jwt import PyJWTCodec
from es.agent import ElasticsearchAgent

pyjwt_codec = PyJWTCodec(single=True)
elasticsearch_agent = ElasticsearchAgent(single=True, client=Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS,
                                                                           port=settings.ELASTICSEARCH_PORT))

app_name = 'outings'
urlpatterns = [
    path('/outing-cards', views.OutingApplyFromStudent.as_view(
        jwt_codec=pyjwt_codec,
    )),
    path('/outing-cards/_search', views.OutingsSearch.as_view(
        jwt_codec=pyjwt_codec,
        elasticsearch_agency=elasticsearch_agent,
    )),
]
