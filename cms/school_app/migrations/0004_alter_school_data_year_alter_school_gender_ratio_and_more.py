# Generated by Django 4.0.3 on 2022-04-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_alter_school_lat_alter_school_lon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='data_year',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='gender_ratio',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='test_score',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='total_enrollment',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
    ]
