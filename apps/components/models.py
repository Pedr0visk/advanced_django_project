from django.db import models
from apps.subsystems.models import Subsystem


# Create your models here.
class Component(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    subsystem = models.ForeignKey(Subsystem, on_delete=models.CASCADE, related_name='components')

    def __str__(self):
        return self.name
