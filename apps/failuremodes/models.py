from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.components.models import Component
from apps.bops.models import TestGroup


# Create your models here.
class FailureMode(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(TestGroup,
                              on_delete=models.DO_NOTHING,
                              blank=True,
                              null=True)
    component = models.ForeignKey(Component,
                                  on_delete=models.CASCADE,
                                  related_name='failures_mode')
    failure_mode = models.ForeignKey('self',
                                     on_delete=models.PROTECT,
                                     related_name='failure_children',
                                     blank=True,
                                     null=True)
    distribution = JSONField(blank=True, null=True)
    diagnostic_coverage = models.FloatField()

    def __str__(self):
        return self.name
