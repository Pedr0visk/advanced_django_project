# Generated by Django 3.0.8 on 2020-09-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_groups', '0009_remove_testgrouphistory_bop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testgrouphistory',
            name='event',
            field=models.CharField(choices=[('Created', 'Created'), ('Updated', 'Updated'), ('Deleted', 'Deleted')], default='Updated', max_length=7),
        ),
    ]