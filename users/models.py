from django.db import models
from django.core import validators
from postgres_composite_types import CompositeType


class StudentNumber(CompositeType):
    """custom composite type for postgresql field having grade, group, number value

    (SQL in postgresql)
    CREATE TYPE "student_number" AS ("grade" smallint, "group" smallint, "number" smallint);
    """

    # grade(학년) value of student number type (postgresql -> "grade" smallint)
    grade = models.SmallIntegerField(null=True, validators=[
        validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=3),  # 1~3 between value
    ])
    # group(반) value of student number type (postgresql -> "group" smallint)
    group = models.SmallIntegerField(null=True, validators=[
        validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=4),  # 1~4 between value
    ])
    # number(번호) value of student number type (postgresql -> "number" smallint)
    number = models.SmallIntegerField(null=True, validators=[
        validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=21),  # 1~21 between value
    ])

    class Meta:
        # set type name of StudentNumber in postgresql
        db_type = 'student_number'


class Students(models.Model):
    """Students model having account value(uuid, id, pw) and student inform(number, phone, etc ...)

    (SQL in postgresql)
    CREATE TABLE "users_students" (
        "uuid"             varchar(20) NOT NULL PRIMARY KEY,
        "student_id"       varchar(20) NOT NULL UNIQUE,
        "student_pw"       text NOT NULL,
        "student_number"   student_number NULL,
        "name"             varchar(10) NOT NULL,
        "phone_number"     varchar(11) NOT NULL UNIQUE,
        "profile_uri_path" text NOT NULL UNIQUE
    );
    """

    # primary key of Students model (postgresql -> "uuid" varchar(20) NOT NULL PRIMARY KEY))
    uuid = models.CharField(primary_key=True, max_length=20, validators=[
        validators.RegexValidator(regex='^student-\\d{12}$'),  # check uuid value with regular expression
    ])

    # id value of student account (postgresql -> varchar(20) NOT NULL UNIQUE)
    student_id = models.CharField(max_length=20, unique=True)

    # hashed password value of student account (postgresql -> text NOT NULL)
    student_pw = models.TextField()

    # student number value contains grade, group, number of student (postgresql -> student_number NULL)
    student_number = StudentNumber.Field(blank=True)

    # name value of student inform (postgresql -> varchar(10) NOT NULL)
    name = models.CharField(max_length=10)

    # phone number value of student inform (postgresql -> varchar(11) NOT NULL UNIQUE)
    phone_number = models.CharField(max_length=11, unique=True, validators=[
        validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')  # check phone number value with regular expression
    ])

    # path value in profile uri of student profile (postgresql -> text NOT NULL UNIQUE)
    profile_uri_path = models.TextField(unique=True)

    def save(self, *args, **kwargs):
        """overriding save method used when create or update instance with Students model"""

        # initialize self.student_number if is None or empty tuple
        if self.student_number is None or self.student_number == ():
            self.student_number = None, None, None

        if isinstance(self.student_number, tuple):
            self.student_number = self.student_number + (None, ) * (3 - len(self.student_number))

        return super(Students, self).save(*args, **kwargs)
