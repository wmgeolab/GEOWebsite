import django_filters
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


class School(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.TextField()
    data_year = models.IntegerField(null=True)
    school_name = models.TextField()
    sector = models.TextField(blank=True)
    school_level = models.TextField(blank=True)
    municipality = models.TextField(blank=True)
    department = models.TextField(blank=True)
    zone = models.TextField(blank=True)
    address = models.TextField(blank=True)
    total_enrollment = models.IntegerField(null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    test_score = models.FloatField(null=True)
    gender_ratio = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.school_name

    class Meta:
        db_table = "schools"


STATUS = ((0, "Draft"), (1, "Publish"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


# Filters

COUNTRIES = [
    ("South Africa", "South Africa"),
    ("Peru", "Peru"),
    ("Paraguay", "Paraguay"),
    ("Bahrain", "Bahrain"),
    ("Colombia", "Colombia"),
    ("Costa Rica", "Costa Rica"),
    ("Guatemala", "Guatemala"),
    ("Panama", "Panama"),
    ("Mexico", "Mexico"),
]


class SchoolResourcesFilter(django_filters.FilterSet):

    country = django_filters.ChoiceFilter(choices=COUNTRIES)

    class Meta:
        model = School
        db_table = "schools"

        fields = {
            "school_name": ["icontains"],
            #'country': ['icontains'],
            "municipality": ["icontains"],
            "department": ["icontains"],
            "sector": ["icontains"],
        }
