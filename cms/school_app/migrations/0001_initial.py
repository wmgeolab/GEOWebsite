# Generated by Django 4.0.3 on 2022-04-05 15:29

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('country', models.TextField()),
                ('data_year', models.IntegerField(null=True)),
                ('school_name', models.TextField()),
                ('sector', models.TextField(blank=True)),
                ('school_level', models.TextField(blank=True)),
                ('municipality', models.TextField(blank=True)),
                ('department', models.TextField(blank=True)),
                ('zone', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('total_enrollment', models.IntegerField(null=True)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('test_score', models.FloatField(null=True)),
                ('gender_ratio', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'schools',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
