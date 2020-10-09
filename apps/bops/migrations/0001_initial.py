# Generated by Django 3.0.8 on 2020-10-09 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SafetyFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('bop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='safety_functions', to='bops.Bop')),
            ],
        ),
        migrations.AddField(
            model_name='bop',
            name='rig',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bops.Rig'),
        ),
    ]
