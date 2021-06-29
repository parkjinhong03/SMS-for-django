from rest_framework import serializers
from .models import OutingCards


class OutingsSearch:
    class GET(serializers.ModelSerializer):
        start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        arrival_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

        class Meta:
            model = OutingCards
            fields = ('uuid', 'student_uuid', 'progress', 'accepted_teacher', 'is_emergency', 'start_time', 'end_time',
                      'arrival_time', 'reason', 'place')  # 'lat', 'lon'
