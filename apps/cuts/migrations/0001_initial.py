# Generated by Django 3.0.8 on 2020-10-13 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField()),
                ('order', models.BigIntegerField()),
                ('failure_modes', models.TextField()),
                ('safety_function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuts', to='bops.SafetyFunction')),
            ],
        ),
    ]
