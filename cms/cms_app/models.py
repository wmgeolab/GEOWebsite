from django.db import models
import django_filters


class School(models.Model):
    country = models.TextField()
    school_id = models.IntegerField(unique=True)
    remoteness_index = models.FloatField()
    total_recieving_cct = models.IntegerField()
    cct_percentage = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    original_water_boolean = models.IntegerField()
    original_internet_boolean = models.IntegerField()
    original_electricity_boolean = models.IntegerField()
    classroom_count = models.IntegerField()
    student_classroom_ratio = models.FloatField()
    total_teachers = models.IntegerField()
    student_teacher_ratio = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    school_name = models.TextField()
    region = models.TextField()
    division = models.TextField()
    province = models.TextField()
    municipality = models.TextField()
    district = models.TextField()
    total_female = models.IntegerField()
    total_male = models.IntegerField()
    total_enrollment = models.IntegerField()


# Filters
class SchoolResourcesFilter(django_filters.FilterSet):

    class Meta:
        model = School

        fields = {
            'school_name': ['icontains'],
            'region': ['icontains'],
            'district': ['icontains'],
            'division': ['icontains'],
            'province': ['icontains']
        }
