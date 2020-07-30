from django.db import models
from apps.bops.models import Bop

class Certification(models.Model):
  bop = models.ForeignKey(Bop, on_delete=models.CASCADE)
  code = models.CharField(max_length=255)
  expiry_date = models.DateField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.code