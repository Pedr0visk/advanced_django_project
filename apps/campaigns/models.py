from django.db import models
from apps.bops.models import Bop

class Campaign(models.Model):

  class StatusCampaign(models.TextChoices):
    GREEN   = 'Green'
    YELLOW  = 'Yellow'
    ORANGE  = 'Orange'
    RED     = 'Red'

  name = models.CharField(max_length=100)
  bop = models.ForeignKey(Bop, on_delete=models.PROTECT)
  active = models.BooleanField(default=True)
  rig_name = models.CharField(max_length=100, null=True)
  description = models.TextField(blank=True, null=True)

  status = models.CharField(
    max_length=6,
    choices=StatusCampaign.choices,
    default=StatusCampaign.GREEN
  )

  start_date  = models.DateField()
  end_date = models.DateField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
