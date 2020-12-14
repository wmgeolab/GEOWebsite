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



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


YEAR_CHOICES = (
    (2015, '2015 - 2016'),
    (2016, '2016 - 2017'),
    (2017, '2017 - 2018'),
)


# Filters
class SchoolResourcesFilter(django_filters.FilterSet):
    school_year = django_filters.ChoiceFilter(choices=YEAR_CHOICES)
    school_name = django_filters.CharFilter(field_name = 'school_name', lookup_expr = 'icontains')
    region = django_filters.CharFilter(field_name = 'region', lookup_expr = 'icontains')
    district = django_filters.CharFilter(field_name = 'district', lookup_expr = 'icontains')
    division = django_filters.CharFilter(field_name = 'division', lookup_expr = 'icontains')
    province = django_filters.CharFilter(field_name = 'province', lookup_expr = 'icontains')

    class Meta:
        model = Alldata
        fields = ['school_year', 'school_name', 'region', 'district', 'division', 'province']# This is an auto-generated Django model module created by ogrinspect.





# class F(FilterSet):
#     status = ChoiceFilter(choices=STATUS_CHOICES)
#     class Meta:
#         model = User
#         fields = ['status']