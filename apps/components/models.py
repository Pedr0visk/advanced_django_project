from django.db import models
from apps.subsystems.models import Subsystem


# Create your models here.
class Component(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    subsystem = models.ForeignKey(Subsystem, on_delete=models.CASCADE, related_name='components')

    def save(self, *args, **kwargs):
        self.slug = self.code.lower().replace('_', '-')
        super(Component, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
