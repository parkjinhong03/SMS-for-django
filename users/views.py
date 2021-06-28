import datetime
from typing import List, Dict

from django.db import transaction
from django.conf import settings
from rest_framework import generics, mixins
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import APIView
from rest_framework.request import Request

from . import requests, interfaces
from .models import Students
from .serializers import StudentsSerializer
from .permissions import IsAuthenticated, IsUUIDOwner
from app.responses import Response
from app.exceptions import (
    UnexpectedValidateError, RequestInvalidError, UnexpectedError
)
from app.views import Base


class StudentBasicSignup(Base,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    """handle basic sign up of student with create generic api"""

    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    dependency_interfaces = (interfaces.HashingCodec, interfaces.ObjectStorage)

    @classmethod
    def as_view(cls, hashing_codec, object_storage, **initkwargs):
        cls.dependency_duck_typing(hashing_codec, object_storage)

        cls.hashing_codec = hashing_codec
        cls.object_storage = object_storage

        return super(StudentBasicSignup, cls).as_view(**initkwargs)

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        req_serializer = requests.StudentBasicSignupRequest.POST(data=request.data)
        if not req_serializer.is_valid():
            raise RequestInvalidError(req_serializer.errors)

        data = req_serializer.data
        data['uuid'] = Students.get_available_uuid()
        data['student_pw'] = self.hashing_codec.encode(data['student_pw'])

        if 'profile' in request.FILES and (profile := request.FILES['profile']):
            data['profile_uri_path'] = Students.get_profile_uri_path(data['uuid'])

        (student_serializer := StudentsSerializer(data=data)).is_valid()
        validate_errors = contain_code_to_error_string(student_serializer.errors)

        for error in validate_errors.pop('student_id', default=()):
            if (code := error.code) == 'unique':
                return Response(status=409, code=-101, msg='duplicate student id')
            else:
                raise UnexpectedValidateError('student_id', validate_errors)

        for error in validate_errors.pop('phone_number', default=()):
            if (code := error.code) == 'unique':
                return Response(status=409, code=-102, msg='duplicate phone number')
            else:
                raise UnexpectedValidateError('phone_number', validate_errors)

        if validate_errors:
            raise UnexpectedValidateError('unexpected fields', validate_errors)

        tx = transaction.savepoint()

        try:
            self.perform_create(student_serializer.save())
        except Exception as e:
            transaction.savepoint_rollback(tx)
            raise UnexpectedError(e, 'unable to create new student')

        try:
            self.object_storage.put_object(request.FILES['profile'], data['profile_uri_path'])
        except KeyError as e:
            if (e.args[0] if len(e.args) > 0 else '') not in ('profile', 'profile_uri_path'):
                raise UnexpectedError(e, 'unable to upload profile to file storage with KeyError')
        except Exception as e:
            transaction.savepoint_rollback(tx)
            raise UnexpectedError(e, 'unable to upload profile to file storage')

        transaction.savepoint_commit(tx)

        return Response(status=201, msg="succeed to create new student with basic signup", data={
            'student': student_serializer.validated_data,
        })


class StudentBasicLogin(Base,
                        APIView):
    """handle basic login of student account with API View"""

    dependency_interfaces = (interfaces.HashingCodec, interfaces.JWTCodec)

    @classmethod
    def as_view(cls, hashing_codec, jwt_codec, **initkwargs):
        cls.dependency_duck_typing(hashing_codec, jwt_codec)

        cls.hashing_codec = hashing_codec
        cls.jwt_codec = jwt_codec

        return super(StudentBasicLogin, cls).as_view(**initkwargs)

    def post(self, request: Request, *args, **kwargs):
        req_serializer = requests.StudentBasicLoginRequest.POST(data=request.data)
        if not req_serializer.is_valid():
            raise RequestInvalidError(req_serializer.errors)
        data = req_serializer.data

        try:
            student = Students.objects.get(student_id=data['student_id'])
            if not self.hashing_codec.compare_hash(data['student_pw'], student.student_pw):
                return Response(status=409, code=-111, msg='incorrect student account id or pw')
        except Students.DoesNotExist:
            return Response(status=409, code=-111, msg='incorrect student account id or pw')
        except Exception as e:
            raise UnexpectedError(e, 'unexpected error occurs while getting student with student id')

        return Response(status=200, msg='succeed to login student account', data={
            'student_uuid': student.uuid,
            'access_token': self.jwt_codec.encode(payload={
                'uuid': student.uuid,
                'type': 'access_token',
            }, key=settings.JWT_SECRET_KEY, expired_at=datetime.datetime.utcnow() + datetime.timedelta(weeks=2)),
        })


class StudentDetail(Base,
                    APIView):
    """handle about student detail logic (ex, get & update & delete ...)"""

    dependency_interfaces = (interfaces.JWTCodec, )
    permission_classes = [IsAuthenticated, IsUUIDOwner]

    @classmethod
    def as_view(cls, jwt_codec, **initkwargs):
        cls.dependency_duck_typing(jwt_codec)

        cls.jwt_codec = jwt_codec

        return super(StudentDetail, cls).as_view(**initkwargs)

    def get(self, request: Request, student_uuid: str, *args, **kwargs):
        try:
            student = Students.objects.get(uuid=student_uuid)
        except Students.DoesNotExist:
            return Response(status=404, msg='student with that uuid is not exist')
        except Exception as e:
            raise UnexpectedError(e, 'unexpected error occurs while getting student with student uuid')

        student_data = StudentsSerializer(student).data
        student_data.pop('student_id')
        student_data.pop('student_pw')

        return Response(status=200, msg='succeed to get student inform with student uuid', data=student_data)


class StudentDetailPassword(Base,
                            APIView):
    """handle about student detail password logic"""

    dependency_interfaces = (interfaces.HashingCodec, interfaces.JWTCodec)
    permission_classes = [IsAuthenticated, IsUUIDOwner]

    @classmethod
    def as_view(cls, hashing_codec, jwt_codec, **initkwargs):
        cls.dependency_duck_typing(hashing_codec, jwt_codec)

        cls.hashing_codec = hashing_codec
        cls.jwt_codec = jwt_codec

        return super(StudentDetailPassword, cls).as_view(**initkwargs)

    @transaction.atomic
    def put(self, request, student_uuid: str, *args, **kwargs):
        req_serializer = requests.StudentDetailPassword.PUT(data=request.data)
        if not req_serializer.is_valid():
            raise RequestInvalidError(req_serializer.errors)
        data = req_serializer.data

        try:
            student = Students.objects.get(uuid=student_uuid)
        except Students.DoesNotExist:
            return Response(status=404, msg='student with that uuid is not exist')
        except Exception as e:
            raise UnexpectedError(e, 'unexpected error occurs while getting student with student uuid')

        if not self.hashing_codec.compare_hash(data['current_pw'], student.student_pw):
            return Response(status=409, code=-121, msg='incorrect current pw')
        student.student_pw = self.hashing_codec.encode(data['revision_pw'])

        tx = transaction.savepoint()
        try:
            student.save()
        except Exception as e:
            transaction.savepoint_rollback(tx)
            raise UnexpectedError(e, 'unable to update student inform')
        transaction.savepoint_commit(tx)

        return Response(status=200, msg='succeed to change student account password')


def contain_code_to_error_string(detail_errors: Dict[str, List[ErrorDetail]]) -> Dict[str, List[ErrorDetail]]:
    for key, errors in detail_errors.items():
        for i, error in enumerate(errors):
            detail_errors[key][i] = ErrorDetail(f'{error} (code: {error.code})', error.code)
    return detail_errors
