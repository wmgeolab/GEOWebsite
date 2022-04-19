# Generated by Django 4.0.3 on 2022-04-07 22:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0006_alter_schoolv2session_gender_ratio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolv2',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=7, null=True, validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)]),
        ),
        migrations.AlterField(
            model_name='schoolv2',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)]),
        ),
        migrations.AlterField(
            model_name='schoolv2session',
            name='data_year',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='schoolv2session',
            name='gender_ratio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolv2session',
            name='test_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolv2session',
            name='total_enrollment',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]