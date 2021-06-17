from rest_framework import serializers
from .models import Students


class StudentsSerializer(serializers.ModelSerializer):
    """Students model serializer to serialize/deserialize model to data/data to model"""

    grade = serializers.IntegerField(source='student_number.grade')
    group = serializers.IntegerField(source='student_number.group')
    number = serializers.IntegerField(source='student_number.number')

    class Meta:
        model = Students
        fields = ('uuid', 'student_id', 'student_pw', 'grade', 'group', 'number',
                  'name', 'phone_number', 'profile_uri_path')
