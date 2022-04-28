# Generated by Django 4.0.3 on 2022-04-28 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0010_schoolv2_country_unique_id_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='schoolv2',
            index=models.Index(fields=['country', 'school_id'], name='school_idx'),
        ),
        migrations.AddIndex(
            model_name='schoolv2session',
            index=models.Index(fields=['school', 'data_year'], name='session_idx'),
        ),
    ]
