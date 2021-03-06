# Generated by Django 3.0.8 on 2020-10-31 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

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
                ('object_code', models.CharField(blank=True, max_length=255)),
                ('type', models.CharField(choices=[('CRIR', 'Repair in Component'), ('SRIR', 'Repair in Subsystem'), ('CRCE', 'Replace in Component'), ('SRCE', 'Replace in Subsystem'), ('WAW', 'Withdraw'), ('RLL', 'Reinstall'), ('FIL', 'Failure in Failure Mode'), ('CIL', 'Failure in Component'), ('SIL', 'Failure in Subsystem')], default='WAW', max_length=14)),
                ('date', models.DateTimeField()),
                ('campaign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='campaigns.Campaign')),
            ],
        ),
    ]
