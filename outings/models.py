import random
from django.db import models
from django.core import validators
from django.contrib.gis.db import models as gis_model


class OutingCards(models.Model):
    """Outings model having about outing card value

    (SQL in postgresql)
    CREATE TABLE "outings_outingcards" (
        "created_at" timestamp with time zone NOT NULL,
        "updated_at" timestamp with time zone NOT NULL,
        "uuid" varchar(24) NOT NULL PRIMARY KEY,
        "progress" smallint NOT NULL,
        "is_emergency" boolean NOT NULL,
        "start_time" timestamp with time zone NOT NULL,
        "end_time" timestamp with time zone NOT NULL,
        "arrival_time" timestamp with time zone NULL,
        "reason" varchar(1000) NOT NULL,
        "place" varchar(200) NOT NULL,
        "place_point" geometry(POINT,4326) NOT NULL,
        "accepted_teacher_id" varchar(20) NULL,
        "student_uuid_id" varchar(20) NOT NULL
    );
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
    student_uuid = models.ForeignKey(to='users.Students', on_delete=models.CASCADE, related_name='apply_outings',
                                     db_column='student_uuid')
    progress = models.SmallIntegerField(default=Progresses.APPLIED)
    accepted_teacher = models.ForeignKey(to='users.Teachers', on_delete=models.CASCADE,
                                         related_name='accept_outings', null=True, db_column='accepted_teacher')
    is_emergency = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True)
    reason = models.CharField(max_length=1000)
    place = models.CharField(max_length=200)
    place_point = gis_model.PointField()

    def save(self, *args, **kwargs):
        self.uuid = self.uuid if self.uuid else self.get_available_uuid()
        return super(OutingCards, self).save(*args, **kwargs)

    @classmethod
    def get_available_uuid(cls) -> str:
        while OutingCards.objects.filter(uuid=(uuid := cls.generate_random_uuid())):
            continue
        return uuid

    @classmethod
    def generate_random_uuid(cls) -> str:
        rand = str(random.randint(0, 999999999999))
        uuid_number = '0' * (12 - len(rand)) + rand
        return f'outing_card-{uuid_number}'
