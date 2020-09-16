# Generated by Django 3.0.8 on 2020-09-15 15:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_groups', '0006_auto_20200915_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testgrouphistory',
            name='test_group',
        ),
        migrations.RemoveField(
            model_name='testgrouphistory',
            name='testgroup_ptr',
        ),
        migrations.AddField(
            model_name='testgroup',
            name='deleted_at',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2020-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='event',
            field=models.CharField(choices=[('C', 'Created'), ('U', 'Updated'), ('D', 'Deleted')], default='U', max_length=1),
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='failure_modes',
            field=models.TextField(default='1,2,3,4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='start_date',
            field=models.DateField(default='2020-02-02'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='test_group_id',
            field=models.BigIntegerField(default=31),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testgrouphistory',
            name='tests',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]