# Generated by Django 3.0.3 on 2020-07-30 12:54

import chemreg.common.utils
import chemreg.common.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('substance', '0004_lich_sprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='substance',
            name='qc_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.QCLevelsType', validators=[chemreg.common.validators.validate_deprecated]),
        ),
        migrations.AlterField(
            model_name='substance',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.Source', validators=[chemreg.common.validators.validate_deprecated]),
        ),
        migrations.AlterField(
            model_name='substance',
            name='substance_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.SubstanceType', validators=[chemreg.common.validators.validate_deprecated]),
        ),
        migrations.AlterField(
            model_name='synonym',
            name='qc_notes',
            field=models.TextField(blank=True, default='', max_length=1024),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='SubstanceRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qc_note', models.CharField(blank=True, max_length=1024)),
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
