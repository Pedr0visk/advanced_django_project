# Generated by Django 3.0.8 on 2021-01-26 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0015_auto_20210114_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schema_clones', to='campaigns.Schema'),
        ),
    ]
