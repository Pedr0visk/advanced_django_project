# Generated by Django 3.0.8 on 2020-08-31 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='campaigns.Campaign')),
            ],
        ),
    ]
