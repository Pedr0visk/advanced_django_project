from django.db import models

from apps.bops.models import Bop
from apps.failuremodes.models import FailureMode
from apps.tests.models import Test


class TestGroup(models.Model):
    start_date = models.DateField()
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE)
    tests = models.ManyToManyField(Test, related_name='groups')
    failure_modes = models.ManyToManyField(FailureMode, related_name='groups')

    def __str__(self):
        return f'group {self.id}'
