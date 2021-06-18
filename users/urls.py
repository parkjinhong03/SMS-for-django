from django.urls import path
from . import views
from hash import bcrypt

app_name = 'users'
urlpatterns = [
    path('students', views.StudentBasicSignup.as_view(
        hashing_codec=bcrypt.BcryptHashingCodec(),
    ), name='student-basic-sign-up'),
]
