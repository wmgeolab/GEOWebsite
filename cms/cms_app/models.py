from django.db import models
import django_filters


class Alldata(models.Model):
    school_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    school_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    cluster = models.TextField(blank=True, null=True)
    remoteness_index = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_recieving_cct = models.TextField(blank=True, null=True)  # This field type is a guess.
    cct_percentage = models.TextField(blank=True, null=True)  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)
    original_water_boolean = models.TextField(blank=True, null=True)  # This field type is a guess.
    nowater = models.TextField(blank=True, null=True)  # This field type is a guess.
    original_internet_boolean = models.TextField(blank=True, null=True)  # This field type is a guess.
    no_internet = models.TextField(blank=True, null=True)  # This field type is a guess.
    noelec = models.TextField(blank=True, null=True)  # This field type is a guess.
    original_electricity_boolean = models.TextField(blank=True, null=True)  # This field type is a guess.
    instructional_rooms = models.TextField(blank=True, null=True)  # This field type is a guess.
    student_classroom_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_teachers = models.TextField(blank=True, null=True)  # This field type is a guess.
    student_teacher_ratio = models.TextField(blank=True, null=True)  # This field type is a guess.
    accessibility = models.TextField(blank=True, null=True)  # This field type is a guess.
    amenities = models.TextField(blank=True, null=True)  # This field type is a guess.
    conditions = models.TextField(blank=True, null=True)  # This field type is a guess.
    shi_score = models.TextField(blank=True, null=True)  # This field type is a guess.
    latitude = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude = models.TextField(blank=True, null=True)  # This field type is a guess.
    school_name = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    division = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    municipality = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    total_female = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_male = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_enrollment = models.TextField(blank=True, null=True)  # This field type is a guess.
    ds_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    cp_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    dcm_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    drcpau_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    dh_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    autism_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    wcg_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    eb_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    hi_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    li_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    md_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    shp_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    speech_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    vi_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    ii_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    pwd_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    id = models.TextField(primary_key=True, blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'AllData'


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





# Filters
class SchoolResourcesFilter(django_filters.FilterSet):
    school_year = django_filters.NumberFilter()
    school_name = django_filters.CharFilter(field_name = 'school_name', lookup_expr = 'icontains')
    region = django_filters.CharFilter(field_name = 'region', lookup_expr = 'icontains')
    district = django_filters.CharFilter(field_name = 'district', lookup_expr = 'icontains')
    division = django_filters.CharFilter(field_name = 'division', lookup_expr = 'icontains')
    province = django_filters.CharFilter(field_name = 'province', lookup_expr = 'icontains')

    class Meta:
        model = Alldata
        fields = ['school_year', 'school_name', 'region', 'district', 'division', 'province']# This is an auto-generated Django model module created by ogrinspect.



