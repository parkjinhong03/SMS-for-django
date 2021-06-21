from django.urls import path
from . import views
from codec import hash, jwt
from storage import s3

hashing_codec = hash.BcryptHashingCodec()
object_storage = s3.S3Storage()
jwt_codec = jwt.PyJWTCodec()

app_name = 'users'
urlpatterns = [
    path('students', views.StudentBasicSignup.as_view(
        hashing_codec=hashing_codec,
        object_storage=object_storage,
    ), name='student-basic-sign-up'),

    path('login/students', views.StudentBasicLogin.as_view(
        hashing_codec=hashing_codec,
        jwt_codec=jwt_codec,
    ), name='student-basic-login')
]
