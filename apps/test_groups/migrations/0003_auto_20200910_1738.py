# Generated by Django 3.0.8 on 2020-09-10 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bops', '0001_initial'),
        ('failuremodes', '0002_remove_failuremode_groups'),
        ('test_groups', '0002_auto_20200910_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='testgroup',
            name='bop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bops.Bop'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testgroup',
            name='failure_modes',
            field=models.ManyToManyField(related_name='groups', to='failuremodes.FailureMode'),
        ),
    ]