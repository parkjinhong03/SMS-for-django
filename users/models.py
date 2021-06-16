from django.db import models
from django.core.validators import RegexValidator
from postgres_composite_types import CompositeType


class Students(models.Model):
    """Students model having account value(uuid, id, pw) and student inform(number, phone, etc ...)"""

    # primary key of Students model
    # postgresql -> "uuid" varchar(20) NOT NULL PRIMARY KEY)
    uuid = models.CharField(primary_key=True, max_length=20, validators=[
        RegexValidator(regex='^student-\\d{12}'),  # check uuid value with '^student-\d{12}' regex
    ])

    # id value of student account
    student_id = models.CharField(max_length=20, unique=True)

    # hashed password value of student account
    student_pw = models.TextField()
