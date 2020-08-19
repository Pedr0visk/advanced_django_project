from django.db import models
from apps.campaigns.models import Campaign


class Well(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.name
