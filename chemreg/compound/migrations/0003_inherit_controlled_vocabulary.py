# Generated by Django 3.0.3 on 2020-06-04 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compound', '0002_alter_cid_inchikey'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='querystructuretype',
            options={},
        ),
        migrations.AddField(
            model_name='querystructuretype',
            name='deprecated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='querystructuretype',
            name='label',
            field=models.CharField(max_length=99, unique=True),
        ),
        migrations.AlterField(
            model_name='querystructuretype',
            name='long_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='querystructuretype',
            name='name',
            field=models.SlugField(max_length=49, unique=True),
        ),
        migrations.AlterField(
            model_name='querystructuretype',
            name='short_description',
            field=models.CharField(max_length=499),
        ),
    ]