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

    class StudentNumber(CompositeType):
        """composite type for postgresql field having grade, group, number value"""
        grade = models.SmallIntegerField()   # grade(학년) value of student number type
        group = models.SmallIntegerField()   # group(반) value of student number type
        number = models.SmallIntegerField()  # number(번호) value of student number type

        class Meta:
            db_type = 'student_number'

    # student number value contains grade, group, number of student
    student_number = StudentNumber.Field()

    # def save(self, *args, **kwargs):
    #     student_number = self.student_number
    #     self.student_number = (student_number['grade'], student_number['group'], student_number['number'])
    #     return super(Students, self).save(*args, **kwargs)
