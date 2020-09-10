from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.components.models import Component


class FailureMode(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    component = models.ForeignKey(Component,
                                  on_delete=models.CASCADE,
                                  related_name='failure_modes')

    failure_mode = models.ForeignKey('self',
                                     on_delete=models.PROTECT,
                                     related_name='failure_children',
                                     blank=True,
                                     null=True)

    distribution = JSONField(blank=True, null=True)
    diagnostic_coverage = models.FloatField()
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.code.lower().replace('_', '-')
        super(FailureMode, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
