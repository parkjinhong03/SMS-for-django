import random
from django.db import models
from django.core import validators
from postgres_composite_types import CompositeType


class Students(models.Model):
    """Students model having account value(uuid, id, pw) and student inform(number, phone, etc ...)

    (SQL in postgresql)
    CREATE TABLE "users_students" (
        "created_at"       timestamp with time zone DEFAULT NOT NULL
        "updated_at"       timestamp with time zone DEFAULT NOT NULL
        "uuid"             varchar(20) NOT NULL PRIMARY KEY,
        "student_id"       varchar(20) NOT NULL UNIQUE,
        "student_pw"       text NOT NULL,
        "student_number"   student_number NULL,
        "name"             varchar(10) NOT NULL,
        "phone_number"     varchar(11) NOT NULL UNIQUE,
        "profile_uri_path" text NOT NULL UNIQUE
    );
    """

    class StudentNumber(CompositeType):
        """custom composite type for postgresql field having grade, group, number value

        (SQL in postgresql)
        CREATE TYPE "student_number" AS ("grade" smallint, "group" smallint, "number" smallint);
        """

        grade = models.SmallIntegerField(null=True, validators=[
            validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=3),
        ])
        group = models.SmallIntegerField(null=True, validators=[
            validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=4),
        ])
        number = models.SmallIntegerField(null=True, validators=[
            validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=21),
        ])

        class Meta:
            db_type = 'student_number'

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    uuid = models.CharField(primary_key=True, max_length=20, validators=[
        validators.RegexValidator(regex='^student-\\d{12}$'),
    ])
    student_id = models.CharField(max_length=20, unique=True)
    student_pw = models.TextField()
    student_number = StudentNumber.Field(blank=True)
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=11, unique=True, validators=[
        validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')
    ])
    profile_uri_path = models.TextField(unique=True, null=True)

    class Meta:
        ordering = ['uuid']

    def save(self, *args, **kwargs):
        """overriding save method used when create or update instance with Students model"""

        # initialize self.student_number if is None or empty tuple
        if (not self.student_number) or (not isinstance(self.student_number, tuple)):
            self.student_number = None, None, None

        if isinstance(self.student_number, tuple):
            self.student_number = self.student_number + (None, ) * (3 - len(self.student_number))

        self.uuid = self.uuid if self.uuid else Students.get_available_uuid()

        return super(Students, self).save(*args, **kwargs)

    @classmethod
    def get_available_uuid(cls) -> str:
        while Students.objects.filter(uuid=(uuid := cls.generate_random_uuid())):
            continue
        return uuid

    @classmethod
    def generate_random_uuid(cls) -> str:
        rand = str(random.randint(0, 999999999999))
        uuid_number = '0' * (12 - len(rand)) + rand
        return f'student-{uuid_number}'

    @classmethod
    def get_profile_uri_path(cls, uuid: str) -> str:
        return f'profiles/students/uuid/{uuid}'


class Teachers(models.Model):
    """Teachers model having account value(uuid, id, pw) and teacher inform(group, name, phone_number, etc...)

    (SQL in postgresql)
    CREATE TABLE "users_teachers" (
        "created_at" timestamp with time zone NOT NULL,
        "updated_at" timestamp with time zone NOT NULL,
        "uuid" varchar(20) NOT NULL PRIMARY KEY,
        "teacher_id" varchar(20) NOT NULL UNIQUE,
        "teacher_pw" text NOT NULL,
        "teacher_group" teacher_group NOT NULL,
        "name" varchar(10) NOT NULL,
        "phone_number" varchar(11) NOT NULL UNIQUE);
    );
    """

    class TeacherGroup(CompositeType):
        """custom composite type for postgresql field having grade, group value

        (SQL in postgresql)
        CREATE TYPE "teacher_group" AS ("grade" smallint, "group" smallint);
        """

        grade = models.SmallIntegerField(null=True, validators=[
            validators.MinValueValidator(1), validators.MaxValueValidator(3)
        ])
        group = models.SmallIntegerField(null=True, validators=[
            validators.MinValueValidator(1), validators.MaxValueValidator(3)
        ])

        class Meta:
            db_type = 'teacher_group'

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    uuid = models.CharField(primary_key=True, max_length=20, validators=[
        validators.RegexValidator(regex='^teacher-\\d{12}$'),
    ])
    teacher_id = models.CharField(max_length=20, unique=True)
    teacher_pw = models.TextField()
    teacher_group = TeacherGroup.Field(blank=True)
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=11, unique=True, validators=[
        validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')
    ])
