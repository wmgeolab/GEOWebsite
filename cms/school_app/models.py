from django.db import models
import django_filters
from django.contrib.auth.models import User


class School(models.Model):
    country = models.TextField()
    school_id = models.IntegerField(primary_key=True)
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

    def __str__(self) -> str:
        return self.school_name


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

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
