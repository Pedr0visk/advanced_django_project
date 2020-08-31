# Generated by Django 3.0.8 on 2020-08-31 17:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('components', '0001_initial'),
        ('bops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailureMode',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('distribution', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('diagnostic_coverage', models.FloatField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failures_mode', to='components.Component')),
                ('failure_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='failure_children', to='failuremodes.FailureMode')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bops.TestGroup')),
            ],
        ),
    ]
