# Generated by Django 3.0.8 on 2020-11-30 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20201123_1636'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phase',
            options={'ordering': ['start_date']},
        ),
        migrations.AddField(
            model_name='schema',
            name='cuts_contribution',
            field=models.TextField(blank=True, null=True),
        ),
    ]
