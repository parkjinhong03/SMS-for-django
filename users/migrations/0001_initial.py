# Generated by Django 2.2 on 2021-06-17 00:41

import django.core.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        users.models.StudentNumber.Operation(),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('uuid', models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^student-\\d{12}$')])),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('student_pw', models.TextField()),
                ('student_number', users.models.StudentNumber.Field(null=True)),
                ('name', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d{3}\\d{3,4}\\d{4}$')])),
                ('profile_uri_path', models.TextField(unique=True)),
            ],
        ),
    ]