# Generated by Django 3.0.8 on 2020-10-15 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bops', '0001_initial'),
        ('test_groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('well_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Green', 'Green'), ('Yellow', 'Yellow'), ('Orange', 'Orange'), ('Red', 'Red')], default='Green', max_length=6)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='bops.Bop')),
            ],
            options={
                'ordering': ['-active', '-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemas', to='campaigns.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('duration', models.FloatField()),
                ('has_test', models.BooleanField(default=False)),
                ('is_drilling', models.BooleanField(default=False)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='campaigns.Schema')),
                ('test_groups', models.ManyToManyField(related_name='test_groups', to='test_groups.TestGroup')),
            ],
        ),
    ]
