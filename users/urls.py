from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('students', views.StudentBasicSignup.as_view(), name='student-basic-sign-up'),
]
