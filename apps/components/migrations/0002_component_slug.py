# Generated by Django 3.0.8 on 2020-09-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
