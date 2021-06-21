from abc import ABCMeta
from typing import List, Dict

from django.db import transaction
from rest_framework import generics, mixins
from rest_framework.exceptions import ErrorDetail

from . import requests
from .models import Students
from .serializers import StudentsSerializer
from app.responses import Response
from app.exceptions import (
    DependencyNotImplementedError, UnexpectedValidateError, RequestInvalidError, UnexpectedError
)


class HashingCodec(metaclass=ABCMeta):
    """interface to hashing_codec dependency using in View initialize"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'encode') and callable(subclass.encode) or
                hasattr(subclass, 'compare_hash') and callable(subclass.compare_with_hash) or
                NotImplemented)


class ObjectStorage(metaclass=ABCMeta):
    """interface to object_storage dependency using in View initialize"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'put_object') and callable(subclass.put_object) or
                NotImplemented)


class StudentBasicSignup(mixins.CreateModelMixin,
                         generics.GenericAPIView):
    """handle basic sign up of student with create generic api"""
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

    @classmethod
    def as_view(cls, hashing_codec, object_storage, **initkwargs):
        for dependency, interface in (
                (hashing_codec, HashingCodec),
                (object_storage, ObjectStorage),
        ):
            if not isinstance(dependency, interface):
                raise DependencyNotImplementedError(dependency, interface)

        cls.hashing_codec = hashing_codec
        cls.object_storage = object_storage

        return super(StudentBasicSignup, cls).as_view(**initkwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
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
                return Response(status=409, code=-101, msg='duplicate phone number')
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

        return Response(status=201, msg="succeed to create new student with basic sign up")


def contain_code_to_error_string(detail_errors: Dict[str, List[ErrorDetail]]) -> Dict[str, List[ErrorDetail]]:
    for key, errors in detail_errors.items():
        for i, error in enumerate(errors):
            detail_errors[key][i] = ErrorDetail(f'{error} (code: {error.code})', error.code)
    return detail_errors
