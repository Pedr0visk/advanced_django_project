# Generated by Django 3.0.8 on 2020-10-15 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subsystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('bop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsystems', to='bops.Bop')),
            ],
            options={
                'ordering': ('code', 'name'),
            },
        ),
    ]