from rest_framework import serializers
from .models import OutingCards


class OutingCardsSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    end_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = OutingCards
        fields = ('uuid', 'student_uuid', 'progress', 'accepted_teacher', 'is_emergency', 'start_time', 'end_time',
                  'arrival_time', 'reason', 'place', 'place_point')
