from django.db import models
import django_filters


class Alldata(models.Model):
    country = models.TextField()
    school_id = models.IntegerField()
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
    school_name = django_filters.CharFilter(
        field_name='school_name', lookup_expr='icontains')
    region = django_filters.CharFilter(
        field_name='region', lookup_expr='icontains')
    district = django_filters.CharFilter(
        field_name='district', lookup_expr='icontains')
    division = django_filters.CharFilter(
        field_name='division', lookup_expr='icontains')
    province = django_filters.CharFilter(
        field_name='province', lookup_expr='icontains')

    class Meta:
        model = Alldata
        # This is an auto-generated Django model module created by ogrinspect.
        fields = ['school_name',
                  'region', 'district', 'division', 'province']
