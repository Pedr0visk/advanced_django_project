from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.components.models import Component


class FailureMode(models.Model):
    class DistributionsType(models.TextChoices):
        EXPONENTIAL = 'Exponential'
        PROBABILITY = 'Probability'
        STEP = 'Step'
        WEIBULL = 'Weibull'

    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    diagnostic_coverage = models.FloatField()
    distribution = JSONField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    component = models.ForeignKey(Component,
                                  on_delete=models.CASCADE,
                                  related_name='failure_modes')
    failure_mode = models.ForeignKey('self',
                                     on_delete=models.PROTECT,
                                     related_name='failure_children',
                                     blank=True,
                                     null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.code.lower().replace('_', '-')
        super(FailureMode, self).save(*args, **kwargs)

    def get_pfd(self, dt):
        d = self.distribution
        d_type = d['type']
        coverage = self.diagnostic_coverage

        if d_type == self.DistributionsType.EXPONENTIAL:
            rate = d['exponential_failure_rate']
            self.exponential(rate, coverage, dt)

    @staticmethod
    def exponential(rate, coverage, time):
        return rate * coverage * time

    @staticmethod
    def probability(rate, coverage, time):
        return rate * coverage * time

    @staticmethod
    def step(rate, coverage, time):
        return rate * coverage * time

    @staticmethod
    def weibull(rate, coverage, time):
        return rate * coverage * time
