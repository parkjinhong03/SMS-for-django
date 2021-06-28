from django.urls import path
from . import views
from codec.jwt import PyJWTCodec

pyjwt_codec = PyJWTCodec(common=True)

app_name = 'outings'
urlpatterns = [
    path('/', views.OutingApplyFromStudent.as_view(
        jwt_codec=pyjwt_codec
    ))
]
