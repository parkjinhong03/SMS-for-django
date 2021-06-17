from django.db import models
from django.core import validators
from postgres_composite_types import CompositeType


class StudentNumber(CompositeType):
    """custom composite type for postgresql field having grade, group, number value"""
    # grade(학년) value of student number type
    grade = models.SmallIntegerField(null=True, validators=[
        validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=3),
    ])
    # group(반) value of student number type
    group = models.SmallIntegerField(null=True, validators=[
        validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=4),
    ])
    # number(번호) value of student number type
    number = models.SmallIntegerField(null=True, validators=[
        validators.MinValueValidator(limit_value=1), validators.MaxValueValidator(limit_value=21),
    ])

    class Meta:
        # set type name of StudentNumber in postgresql
        db_type = 'student_number'


class Students(models.Model):
    """Students model having account value(uuid, id, pw) and student inform(number, phone, etc ...)"""

    # primary key of Students model
    # postgresql -> "uuid" varchar(20) NOT NULL PRIMARY KEY)
    uuid = models.CharField(primary_key=True, max_length=20, validators=[
        validators.RegexValidator(regex='^student-\\d{12}$'),  # check uuid value with regular expression
    ])

    # id value of student account
    student_id = models.CharField(max_length=20, unique=True)

    # hashed password value of student account
    student_pw = models.TextField()

    # student number value contains grade, group, number of student
    student_number = StudentNumber.Field(blank=True)

    # name value of student inform
    name = models.CharField(max_length=10)

    # phone number value of student inform
    phone_number = models.CharField(max_length=11, unique=True, validators=[
        validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')  # check phone number value with regular expression
    ])

    # path value in profile uri of student profile
    profile_uri_path = models.TextField(unique=True)

    def save(self, *args, **kwargs):
        """overriding save method used when create or update instance with Students model"""

        # initialize self.student_number if is None or empty tuple
        if self.student_number is None or self.student_number == ():
            self.student_number = None, None, None

        if isinstance(self.student_number, tuple):
            self.student_number = self.student_number + (None, ) * (3 - len(self.student_number))

        return super(Students, self).save(*args, **kwargs)
