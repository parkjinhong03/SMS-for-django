from rest_framework.views import APIView
from app.views import Base
from app.exceptions import RequestInvalidError
from app.responses import Response
from users import permissions
from . import requests, interfaces


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

    def post(self, request, *args, **kwargs):
        req_serializer = requests.OutingApplyFromStudent.POST(data=request.data)
        if not req_serializer.is_valid():
            raise RequestInvalidError(req_serializer.errors)
        data = req_serializer.data

        return Response(status=201, msg='succeed to apply new outing from student', data={'request': data})
