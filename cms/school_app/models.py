import django_filters
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SchoolV2(models.Model):
    # primary key is implied
    school_id = models.TextField()
    country = models.TextField()
    school_name = models.TextField()
    sector = models.TextField(blank=True)
    school_level = models.TextField(blank=True)
    municipality = models.TextField(blank=True)
    department = models.TextField(blank=True)
    zone = models.TextField(blank=True)
    address = models.TextField(blank=True)
    lon = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        blank=True,
        null=True,
        validators=[MaxValueValidator(180), MinValueValidator(-180)],
    )
    lat = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        blank=True,
        null=True,
        validators=[MaxValueValidator(90), MinValueValidator(-90)],
    )

    def __str__(self) -> str:
        return self.school_name

    class Meta:
        db_table = "schoolv2"
        verbose_name = "school"
        constraints = [
            models.UniqueConstraint(
                fields=["country", "school_id"], name="country_unique_id"
            )
        ]


class SchoolV2Session(models.Model):
    # primary key is implied
    school = models.ForeignKey(SchoolV2, models.CASCADE, related_name="sessions")
    session = models.TextField(blank=True)
    data_year = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, null=True
    )
    total_enrollment = models.IntegerField(blank=True, null=True)
    test_score = models.FloatField(blank=True, null=True)
    gender_ratio = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.school}_{self.data_year}_{self.session}"

    class Meta:
        db_table = "schoolv2session"
        verbose_name = "school session"
        constraints = [
            models.UniqueConstraint(
                fields=["school", "data_year", "session"],
                name="school_unique_year_session",
            )
        ]


class School(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.TextField()
    data_year = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    school_name = models.TextField()
    sector = models.TextField(blank=True)
    school_level = models.TextField(blank=True)
    municipality = models.TextField(blank=True)
    department = models.TextField(blank=True)
    zone = models.TextField(blank=True)
    address = models.TextField(blank=True)
    total_enrollment = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    lon = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True,
        validators=[MaxValueValidator(180), MinValueValidator(-180)],
    )
    lat = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True,
        validators=[MaxValueValidator(90), MinValueValidator(-90)],
    )
    test_score = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gender_ratio = models.DecimalField(max_digits=10, decimal_places=0, null=True)

    def __str__(self) -> str:
        return self.school_name

    class Meta:
        db_table = "schools"
        verbose_name = "school (old)"
        verbose_name_plural = "schools (old)"


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
        model = SchoolV2
        db_table = "schoolv2"

        fields = {
            "school_name": ["icontains"],
            #'country': ['icontains'],
            "municipality": ["icontains"],
            "department": ["icontains"],
            "sector": ["icontains"],
        }
