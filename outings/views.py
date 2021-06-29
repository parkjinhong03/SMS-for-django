from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction
from rest_framework.views import APIView

from app.views import Base
from app.exceptions import (
    RequestInvalidError, UnexpectedValidateError, UnexpectedError,
    contain_code_to_error_string
)
from app.responses import Response
from users import permissions
from . import requests, interfaces, responses
from .models import OutingCards
from .serializers import OutingCardsSerializer


class OutingApplyFromStudent(Base,
                             APIView):
    """handle logic to register outing applied from student with APIView"""
    dependency_interfaces = (interfaces.JWTCodec, )
    permission_classes = [permissions.IsAuthenticated]

    @classmethod
    def as_view(cls, jwt_codec, **initkwargs):
        cls.dependency_duck_typing(jwt_codec)

        cls.jwt_codec = jwt_codec

        return super(OutingApplyFromStudent, cls).as_view(**initkwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        req_serializer = requests.OutingApplyFromStudent.POST(data=request.data)
        if not req_serializer.is_valid():
            raise RequestInvalidError(req_serializer.errors)

        data = req_serializer.validated_data
        data['uuid'] = OutingCards.get_available_uuid()
        data['student_uuid'] = request.uuid
        data['place_point'] = GEOSGeometry(f'POINT({data.pop("place_lat")} {data.pop("place_lon")})')

        (outing_card_serializer := OutingCardsSerializer(data=data)).is_valid()
        validate_errors = contain_code_to_error_string(outing_card_serializer.errors)

        if validate_errors:
            raise UnexpectedValidateError('unexpected fields', validate_errors)

        if OutingCards.objects.filter(start_time__day=data['start_time'].day):
            return Response(status=407, code=-201, msg='you already apply outing in that day')

        tx = transaction.savepoint()
        try:
            outing_card_serializer.save()
        except Exception as e:
            transaction.savepoint_rollback(tx)
            raise UnexpectedError(e, 'unexpected error occurs while saving new outing card')
        transaction.savepoint_commit(tx)

        return Response(status=201, msg='succeed to apply new outing from student', data={
            'uuid': outing_card_serializer.validated_data['uuid']
        })


class OutingsSearch(Base,
                    APIView):
    """handle logic to search outing using elasticsearch with APIView"""
    dependency_interfaces = (interfaces.JWTCodec, interfaces.ElasticsearchAgency)
    permission_classes = [permissions.IsAuthenticated]

    @classmethod
    def as_view(cls, jwt_codec, elasticsearch_agency, **initkwargs):
        cls.dependency_duck_typing(jwt_codec, elasticsearch_agency)

        cls.jwt_codec = jwt_codec
        cls.elasticsearch_agency = elasticsearch_agency

        return super(OutingsSearch, cls).as_view(**initkwargs)

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)

        es_search_query = \
            {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "reason.nori": query,
                                }
                            } if query else {}
                        ] if query else []
                    }
                }
            }

        try:
            response = self.elasticsearch_agency.search(es_search_query)
            documents = response['hits']['hits']
        except Exception as e:
            raise UnexpectedError(e, 'failed to agent elasticsearch _search command')

        outing_card_uuids = [None] * len(documents)
        for i, document in enumerate(documents):
            outing_card_uuids[i] = document['_id']
        outing_cards = OutingCards.objects.filter(uuid__in=outing_card_uuids)

        return Response(status=200, msg='succeed to search outing card with query', data={
            'total': len(outing_cards),
            'outing_cards': responses.OutingsSearch.GET(outing_cards, many=True).data,
        })
