from django.urls import path
from . import views
from codec import hash, jwt
from storage import s3

bcrypt_codec = hash.BcryptHashingCodec()
s3_storage = s3.S3Storage()
pyjwt_codec = jwt.PyJWTCodec()

app_name = 'users'
urlpatterns = [
    path('students', views.StudentBasicSignup.as_view(
        hashing_codec=bcrypt_codec,
        object_storage=s3_storage,
    ), name='student-basic-sign-up'),

    path('login/students', views.StudentBasicLogin.as_view(
        hashing_codec=bcrypt_codec,
        jwt_codec=pyjwt_codec,
    ), name='student-basic-login'),

    path('students/uuid/<str:student_uuid>', views.StudentDetail.as_view(
        jwt_codec=pyjwt_codec,
    ), name='student-detail-with-uuid'),

    path('students/uuid/<str:student_uuid>/password', views.StudentDetailPassword.as_view(
        hashing_codec=bcrypt_codec,
        jwt_codec=pyjwt_codec,
    ), name='student-detail-with-uuid-password'),
]
