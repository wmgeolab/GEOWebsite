from django.db import models
import django_filters
from django.contrib.auth.models import User


class School(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.TextField()
    data_year = models.IntegerField()
    school_name = models.TextField()
    sector = models.TextField()
    school_level = models.TextField()
    municipality = models.TextField()
    department = models.TextField()
    zone = models.TextField()
    address = models.TextField()
    total_enrollment = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self) -> str:
        return self.school_name

    class Meta:
        managed = False
        db_table = 'schools'

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
        db_table = 'schools'

        fields = {
            'school_name': ['icontains'],
            'country': ['icontains'],
            'municipality': ['icontains'],
            'department': ['icontains'],
            'sector': ['icontains']
        }
