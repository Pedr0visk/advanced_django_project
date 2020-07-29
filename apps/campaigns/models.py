from django.db import models
from django.utils.translation import gettext_lazy as _

class Campaign(models.Model):

  class StatusCampaign(models.TextChoices):
    GREEN   = 1, _('Green')
    YELLOW  = 2, _('Yellow')
    ORANGE  = 3, _('Orange')
    RED     = 4, _('Red')

  name = models.CharField(max_length=100)
  # bop_id = models.ForeignKey(Bop, on_delete=models.PROTECT)
  active = models.BooleanField(default=True)
  rig_name = models.CharField(max_length=100, null=True)
  description = models.TextField(null=True)

  status = models.CharField(
    max_length=1,
    choices=StatusCampaign.choices,
    default=StatusCampaign.GREEN
  )

  start_date = models.DateTimeField()
  end_date = models.DateTimeField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
