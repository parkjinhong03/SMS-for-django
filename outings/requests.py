from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry


class OutingApplyFromStudent:
    """serializer to validate request data used in OutingApplyFromStudent view"""

    class POST(serializers.Serializer):
        start_time = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M",
                                               input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d'])
        end_time = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M",
                                             input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d'])
        reason = serializers.CharField(required=True, max_length=1000)
        place = serializers.CharField(required=True, max_length=200)
        place_x = serializers.FloatField(required=True)
        place_y = serializers.FloatField(required=True)
        is_emergency = serializers.BooleanField(default=False)

        def validate(self, data):
            if not (start_time := data['start_time']) < (end_time := data['end_time']):
                raise serializers.ValidationError({'outing time': 'end_time must be later than start_time'})
            elif start_time.day != end_time.day:
                raise serializers.ValidationError({'outing time': 'end_time and start_time must same day'})
            return data
