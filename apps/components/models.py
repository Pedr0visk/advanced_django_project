from django.db import models
from apps.subsystems.models import Subsystem


# Create your models here.
class Component(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    subsystem = models.ForeignKey(Subsystem, on_delete=models.CASCADE, related_name='components')
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = '{0}-{1}'.format(self.subsystem.id, self.code.lower().replace('_', '-'))
        super(Component, self).save(*args, **kwargs)

    def failure_mode_list(self):
        return self.failure_modes.all()

    def __str__(self):
        return self.name
