from django.db import models
from apps.bops.models import SafetyFunction
from apps.failuremodes.models import FailureMode


class Cut(models.Model):
    index = models.BigIntegerField()
    order = models.BigIntegerField()
    failure_modes = models.TextField()
    safety_function = models.ForeignKey(SafetyFunction,
                                        on_delete=models.CASCADE,
                                        related_name='cuts')
