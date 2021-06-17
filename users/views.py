from django.shortcuts import render
from rest_framework import generics, mixins
from . import requests
from .models import Students
from .serializers import StudentsSerializer
from app.responses import Response


class StudentBasicSignup(BaseView,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    """handle basic sign up of student with create generic api"""
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

    def post(self, request, *args, **kwargs):
        req_serializer = requests.StudentBasicSignupRequest.POST(data=request.data)
        if not req_serializer.is_valid():
            return Response(status=400, msg=req_serializer.errors)
        return Response(status=201)
