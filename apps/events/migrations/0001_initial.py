# Generated by Django 3.0.8 on 2020-09-17 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('RIR', 'Repair'), ('RCE', 'Replace'), ('WAW', 'Withdraw'), ('RLL', 'Reinstall'), ('CIL', 'Failure in Component'), ('FIL', 'Failure in Failure Mode'), ('SIL', 'Failure in Subsystem')], default='RIR', max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('campaign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.Campaign')),
            ],
        ),
    ]
