from django.contrib.admin.utils import NestedObjects
from django.db import models
from django.urls import reverse

from apps.bops.models import Bop
from apps.test_groups.models import TestGroup


class Campaign(models.Model):
    class StatusCampaign(models.TextChoices):
        GREEN = 'Green'
        YELLOW = 'Yellow'
        ORANGE = 'Orange'
        RED = 'Red'

    name = models.CharField(max_length=100)
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE, related_name='campaigns')
    active = models.BooleanField(default=True)
    well_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=6,
        choices=StatusCampaign.choices,
        default=StatusCampaign.GREEN
    )

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_period(self):
        """
        Get the campaign period converted in hours
        :return:
        """
        dt = self.end_date - self.start_date
        days = dt.days
        hours = days * 24
        return days, hours

    def success_url(self):
        return reverse('campaigns:index', args=[self.pk])

    def get_absolute_url(self):
        return reverse('campaigns:index', args=[self.pk])

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
        return model_count.items()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-active', '-start_date']


class Schema(models.Model):
    name = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 related_name='schemas')


class Phase(models.Model):
    name = models.CharField(max_length=255)
    schema = models.ForeignKey(Schema,
                               on_delete=models.CASCADE,
                               related_name='phases')

    test_groups = models.ManyToManyField(TestGroup, related_name='test_groups')
    start_date = models.DateTimeField()
    duration = models.FloatField()
    has_test = models.BooleanField(default=False)
    is_drilling = models.BooleanField(default=False)
