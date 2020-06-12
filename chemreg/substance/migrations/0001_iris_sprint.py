# Generated by Django 3.0.3 on 2020-06-08 20:45

import chemreg.common.utils
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
            name='SubstanceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substancetype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substancetype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='source_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='source_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
    ]