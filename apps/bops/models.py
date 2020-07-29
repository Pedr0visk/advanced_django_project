from django.db import models

class Campaign(models.Model):

  class StatusCampaign(models.TextChoices):
    GREEN = 'G', _('Green')
    YELLOW = 'Y', _('Yellow')
    ORANGE = 'O', _('Orange')
    RED = 'R', _('Red')


  bop_id = models.ForeignKey(Bop, on_delete=models.PROTECT)
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=100, null=True)
  rig_name = models.CharField(max_length=100, null=True)
  active = models.BooleanField(default=True)
  status = models.CharField(
    max_length=1,
    choices=StatusCampaign.choices,
    default=StatusCampaign.GREEN
  )
  start_date = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
  end_date

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
