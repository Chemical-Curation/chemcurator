# Generated by Django 3.0.3 on 2020-06-08 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("compound", "0004_soft_delete_attributes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="basecompound",
            options={"base_manager_name": "objects", "ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="definedcompound",
            options={"base_manager_name": "objects", "ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="illdefinedcompound",
            options={
                "base_manager_name": "objects",
                "ordering": ["pk"],
                "verbose_name": "ill-defined compound",
            },
        ),
        migrations.AlterModelOptions(
            name="querystructuretype",
            options={"base_manager_name": "objects", "ordering": ["pk"]},
        ),
    ]
