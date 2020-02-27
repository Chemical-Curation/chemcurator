# Generated by Django 3.0.3 on 2020-02-26 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compound", "0002_definedcompound"),
    ]

    operations = [
        migrations.CreateModel(
            name="QueryStructureType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.SlugField(
                        help_text="Query structure type name",
                        max_length=49,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        help_text="Query structure type label",
                        max_length=99,
                        unique=True,
                        verbose_name="label",
                    ),
                ),
                (
                    "short_description",
                    models.CharField(
                        help_text="Query structure type short description",
                        max_length=499,
                        verbose_name="short description",
                    ),
                ),
                (
                    "long_description",
                    models.TextField(
                        help_text="Query structure type long description",
                        verbose_name="long description",
                    ),
                ),
            ],
        ),
    ]
