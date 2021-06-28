import random
from django.db import models
from django.core import validators
from django.contrib.gis.db import models as gis_model


class OutingCards(models.Model):
    """Outings model having about outing card value

    (SQL in postgresql)
    """

    class Progresses:
        """
        0 → 외출 신청
        1 → 학부모 승인, -1 → 학부모 거절
        2 → 선생님 승인, -2 → 선생님 거절
        3 → 외출 시작
        4 → 외출 종료
        5 → 외출 인증 승인
        """

        APPLIED = 0
        PARENT_ACCEPTED = 1
        PARENT_REJECTED = -1
        TEACHER_ACCEPTED = 2
        TEACHER_REJECTED = -2
        STARTED = 3
        FINISHED = 4
        CERTIFIED = 5

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    uuid = models.CharField(primary_key=True, max_length=24, validators=[
        validators.RegexValidator(regex='^outing_card-\\d{12}$')
    ])
    student_uuid = models.ForeignKey(to='users.Students', on_delete=models.CASCADE, related_name='apply_outings')
    progress = models.SmallIntegerField(default=Progresses.APPLIED)
    accepted_teacher = models.ForeignKey(to='users.Teachers', on_delete=models.CASCADE,
                                         related_name='accept_outings', null=True)
    is_emergency = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True)
    reason = models.CharField(max_length=1000)
    place = models.CharField(max_length=200)
    place_point = gis_model.PointField()
