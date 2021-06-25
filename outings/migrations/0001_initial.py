# Generated by Django 2.2 on 2021-06-25 01:53

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_teachers'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutingCards',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=24, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^outing_card-\\d{12}$')])),
                ('progress', models.SmallIntegerField()),
                ('is_emergency', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField(null=True)),
                ('reason', models.CharField(max_length=1000)),
                ('outing_place', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('accepted_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accept_outings', to='users.Teachers')),
                ('student_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_outings', to='users.Students')),
            ],
        ),
    ]
