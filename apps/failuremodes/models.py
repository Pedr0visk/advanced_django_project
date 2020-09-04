from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.components.models import Component
from apps.bops.models import TestGroup


# Create your models here.
class FailureMode(models.Model):
    code = models.CharField(max_length=255)
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
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def calculate_pfd(self, step):
        """
        result = 1
        pols = []
        tests = self.group.tests.all() # [{'interval': 168, 'coverage': 0.6}, ...]
        for test in tests:
            sub = 1 - (1 - math.exp((-1) * test.interval * step * (dt) * test.coverage))
            pols.append(sub)

        # pols = [0.234523, 0.53244, 0.12345]

        return 1 - reduce(lambda x, y: x*y), pols)
        """
        return 1

    def save(self, *args, **kwargs):
        self.slug = self.code.lower().replace('_', '-')
        super(FailureMode, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
