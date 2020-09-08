import os

from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.components.models import Component
from apps.bops.models import TestGroup

from library import calc
from functools import reduce


class FailureMode(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(TestGroup,
                              on_delete=models.DO_NOTHING,
                              blank=True,
                              null=True,
                              related_name='failure_modes')

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

    def pdf(self, step):
        result = 1
        pols = []

        for test in self.group.tests.all():
            pols.append(self.test_result(test, step))

        return 1 - reduce((lambda x, y: x * y), pols)

    def test_result(self, test, time):
        type = self.distribution['type']

        if type == 'Exponential':
            return calc.exponential(self.distribution['exponential_failure_rate'], time)

        elif type == 'Probability':
            return calc.exponential(self.distribution['probability'], time)

        elif type == 'Weibull':
            return calc.exponential(self.coverage, test.scale, test.form, time)

        elif type == 'Step':
            return 1

        else:
            return 1

    def save(self, *args, **kwargs):
        self.slug = self.code.lower().replace('_', '-')
        super(FailureMode, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
