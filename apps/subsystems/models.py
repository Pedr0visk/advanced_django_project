from django.db import models
from apps.bops.models import Bop


class Subsystem(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name='subsystems')

    def __str__(self):
        return self.name
