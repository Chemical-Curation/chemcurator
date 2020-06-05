# Generated by Django 3.0.3 on 2020-06-04 21:13

import chemreg.common.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_source_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='source',
            options={},
        ),
        migrations.AddField(
            model_name='source',
            name='deprecated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='source',
            name='label',
            field=models.CharField(max_length=99, unique=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='long_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.SlugField(max_length=49, unique=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='short_description',
            field=models.CharField(max_length=499),
        ),
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
                'abstract': False,
            },
        ),
    ]