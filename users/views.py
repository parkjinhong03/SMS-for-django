from abc import ABCMeta
from rest_framework import generics, mixins
from . import requests
from .models import Students
from .serializers import StudentsSerializer
from app.responses import Response


class HashingCodec(metaclass=ABCMeta):
    """interface to hashing_codec dependency using in View initialize"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'hashpw') and callable(subclass.hashpw) or
                hasattr(subclass, 'checkpw') and callable(subclass.checkpw) or
                NotImplemented)


class StudentBasicSignup(mixins.CreateModelMixin,
                         generics.GenericAPIView):
    """handle basic sign up of student with create generic api"""
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

    @classmethod
    def as_view(cls, hashing_codec, **initkwargs):
        for dependency, interface in (
                (hashing_codec, HashingCodec),
        ):
            if not isinstance(dependency, interface):
                raise DependencyNotImplementedError(dependency, interface)

        cls.hashing_codec = hashing_codec

        return super(StudentBasicSignup, cls).as_view(**initkwargs)

    def post(self, request, *args, **kwargs):
        req_serializer = requests.StudentBasicSignupRequest.POST(data=request.data)
        if not req_serializer.is_valid():
            return Response(status=400, msg=req_serializer.errors)
        return Response(status=201)
