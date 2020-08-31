# Generated by Django 3.0.8 on 2020-08-31 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subsystems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('subsystem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='subsystems.Subsystem')),
            ],
        ),
    ]
