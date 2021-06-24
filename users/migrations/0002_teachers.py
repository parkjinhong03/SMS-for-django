# Generated by Django 2.2 on 2021-06-24 06:00

import django.core.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        users.models.Teachers.TeacherGroup.Operation(),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^teacher-\\d{12}$')])),
                ('teacher_id', models.CharField(max_length=20, unique=True)),
                ('teacher_pw', models.TextField()),
                ('teacher_group', users.models.Teachers.TeacherGroup.Field(blank=True)),
                ('name', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')])),
            ],
        ),
    ]
