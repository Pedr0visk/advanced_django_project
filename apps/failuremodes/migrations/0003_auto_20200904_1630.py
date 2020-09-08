# Generated by Django 3.0.8 on 2020-09-04 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0002_component_slug'),
        ('bops', '0006_safetyfunction_bop'),
        ('failuremodes', '0002_auto_20200901_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='failuremode',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failure_modes', to='components.Component'),
        ),
        migrations.AlterField(
            model_name='failuremode',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='failure_modes', to='bops.TestGroup'),
        ),
    ]
