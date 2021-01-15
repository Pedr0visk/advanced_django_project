# Generated by Django 3.0.8 on 2021-01-14 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_groups', '0003_auto_20201221_1940'),
        ('campaigns', '0014_auto_20210112_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='failures',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='phase',
            name='test_groups',
            field=models.ManyToManyField(to='test_groups.TestGroup'),
        ),
    ]