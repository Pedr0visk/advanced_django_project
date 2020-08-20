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
    rig_name = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=6,
        choices=StatusCampaign.choices,
        default=StatusCampaign.GREEN
    )

    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-active', '-start_date']
