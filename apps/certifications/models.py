from django.db import models
from apps.bops.models import Bop


class Certification(models.Model):
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE, related_name='certifications')
    code = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.code
