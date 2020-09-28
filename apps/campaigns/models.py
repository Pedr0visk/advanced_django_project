from django.db import models
from apps.bops.models import Bop


class Campaign(models.Model):
    class StatusCampaign(models.TextChoices):
        GREEN = 'Green'
        YELLOW = 'Yellow'
        ORANGE = 'Orange'
        RED = 'Red'

    name = models.CharField(max_length=100)
    bop = models.ForeignKey(Bop, on_delete=models.PROTECT, related_name='campaigns')
    active = models.BooleanField(default=True)
    well_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=6,
        choices=StatusCampaign.choices,
        default=StatusCampaign.GREEN
    )

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-active', '-start_date']


class Phase(models.Model):
    class Step(models.TextChoices):
        DESCEND = 1
        CONNECT = 2
        DRILLING = 3
        DISCONNECT = 4

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='phases')
    step = models.IntegerField(choices=Step.choices, default=Step.DESCEND)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    duration = models.FloatField()
