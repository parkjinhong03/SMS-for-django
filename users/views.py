from abc import ABCMeta
from typing import List, Dict

from django.db import transaction
from rest_framework import generics, mixins
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import APIView
from rest_framework.request import Request

from . import requests, interfaces
from .models import Students
from .serializers import StudentsSerializer
from app.responses import Response
from app.exceptions import (
    DependencyNotImplementedError, UnexpectedValidateError, RequestInvalidError, UnexpectedError
)


class BaseView:
    dependency_interface = None

    @classmethod
    def check_dependency_with_interface(cls, *dependency):
        for dependency, interface in zip(dependency, cls.dependency_interface):
            if not isinstance(dependency, interface):
                raise DependencyNotImplementedError(dependency, interface)


class StudentBasicSignup(BaseView,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    """handle basic sign up of student with create generic api"""

    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    dependency_interface = (interfaces.HashingCodec, interfaces.ObjectStorage)

    @classmethod
    def as_view(cls, hashing_codec, object_storage, **initkwargs):
        cls.check_dependency_with_interface(hashing_codec, object_storage)

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



def contain_code_to_error_string(detail_errors: Dict[str, List[ErrorDetail]]) -> Dict[str, List[ErrorDetail]]:
    for key, errors in detail_errors.items():
        for i, error in enumerate(errors):
            detail_errors[key][i] = ErrorDetail(f'{error} (code: {error.code})', error.code)
    return detail_errors
