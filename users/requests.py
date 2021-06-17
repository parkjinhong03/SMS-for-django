from django.core import validators
from rest_framework import serializers


class Validator:
    """implement method which raise NotImplementedError of serializers.Serializer with passing"""
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class StudentBasicSignupRequest:
    """serializer to validate request data used in StudentBasicSignup view"""

    class POST(Validator, serializers.Serializer):
        student_id = serializers.CharField(required=True, min_length=4, max_length=20)
        student_pw = serializers.CharField(required=True, min_length=4, max_length=20)
        grade = serializers.IntegerField(required=False, min_value=1, max_value=3)
        group = serializers.IntegerField(required=False, min_value=1, max_value=4)
        number = serializers.IntegerField(required=False, min_value=1, max_value=21)
        name = serializers.CharField(required=True, max_length=10)
        phone_number = serializers.CharField(required=True, validators=[
            validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')
        ])
