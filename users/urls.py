from django.urls import path
from . import views
from hash import bcrypt
from storage import s3

app_name = 'users'
urlpatterns = [
    path('students', views.StudentBasicSignup.as_view(
        hashing_codec=bcrypt.BcryptHashingCodec(),
        object_storage=s3.S3Storage(),
    ), name='student-basic-sign-up'),
]
