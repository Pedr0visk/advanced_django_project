# Generated by Django 3.0.8 on 2020-08-26 00:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bops', '0004_auto_20200825_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.FloatField()),
                ('coverage', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='failuremode',
            name='distribution',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'type': 'exponential'}),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TestGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tests', models.ManyToManyField(to='bops.Test')),
            ],
        ),
        migrations.AddField(
            model_name='failuremode',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bops.TestGroup'),
        ),
    ]