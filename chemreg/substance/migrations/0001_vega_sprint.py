# Generated by Django 3.0.3 on 2020-11-25 19:33

import chemreg.common.utils
import chemreg.common.validators
import chemreg.substance.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compound', '0001_vega_sprint'),
    ]

    operations = [
        migrations.CreateModel(
            name='QCLevelsType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('rank', models.IntegerField(unique=True)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qclevelstype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qclevelstype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('corrolary_label', models.CharField(max_length=99)),
                ('corrolary_short_description', models.CharField(max_length=499)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='relationshiptype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='relationshiptype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, primary_key=True, serialize=False, unique=True)),
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
            },
        ),
        migrations.CreateModel(
            name='Substance',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(default=chemreg.substance.utils.build_sid, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('preferred_name', models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator("^[a-zA-Z0-9 =<>\\-':.,^%&/{}[\\]()+?=]{3,}$", message="The proposed Preferred Name does not conform to the regular expression ^[a-zA-Z0-9 =<>\\-':.,^%&/{}[\\]()+?=]{3,}$")])),
                ('display_name', models.CharField(max_length=255, null=True, unique=True, validators=[django.core.validators.RegexValidator("^[a-zA-Z0-9 =<>\\-':.,^%&/{}[\\]()+?=]{3,}$", message="The proposed display name does not conform to the regular expression ^[a-zA-Z0-9 =<>\\-':.,^%&/{}[\\]()+?=]{3,}$")])),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('public_qc_note', models.CharField(blank=True, max_length=1024)),
                ('private_qc_note', models.CharField(blank=True, max_length=1024)),
                ('casrn', models.CharField(max_length=50, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{2,7}-[0-9]{2}-[0-9]$', message='The proposed CASRN does not conform to the regular expression ^[0-9]{2,7}-[0-9]{2}-[0-9]$'), chemreg.common.validators.validate_casrn_checksum])),
                ('associated_compound', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substance', to='compound.BaseCompound')),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substance_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('qc_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.QCLevelsType', validators=[chemreg.common.validators.validate_deprecated])),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.Source', validators=[chemreg.common.validators.validate_deprecated])),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SynonymType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('validation_regular_expression', models.TextField(blank=True, validators=[chemreg.common.validators.validate_is_regex])),
                ('score_modifier', models.FloatField(default=0)),
                ('is_casrn', models.BooleanField()),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonymtype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonymtype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SynonymQuality',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('score_weight', models.FloatField(default=1.0)),
                ('is_restrictive', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonymquality_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonymquality_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Synonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.TextField(max_length=1024)),
                ('qc_notes', models.TextField(blank=True, max_length=1024)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonym_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.Source')),
                ('substance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.Substance')),
                ('synonym_quality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.SynonymQuality')),
                ('synonym_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='substance.SynonymType')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonym_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubstanceType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, primary_key=True, serialize=False, unique=True)),
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
            },
        ),
        migrations.AddField(
            model_name='substance',
            name='substance_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.SubstanceType', validators=[chemreg.common.validators.validate_deprecated]),
        ),
        migrations.AddField(
            model_name='substance',
            name='updated_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substance_updated_by_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SubstanceRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qc_notes', models.CharField(blank=True, max_length=1024)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substancerelationship_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('from_substance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='relationships', to='substance.Substance')),
                ('relationship_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.RelationshipType')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.Source')),
                ('to_substance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='related_to', to='substance.Substance')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substancerelationship_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'base_manager_name': 'objects',
                'unique_together': {('from_substance', 'to_substance', 'source', 'relationship_type')},
            },
        ),
    ]