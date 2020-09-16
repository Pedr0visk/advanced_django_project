from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.bops.models import Bop
from apps.failuremodes.models import FailureMode
from apps.tests.models import Test
from datetime import date


class TestGroup(models.Model):
    start_date = models.DateField()
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE)
    failure_modes = models.ManyToManyField(FailureMode, related_name='groups')
    tests = JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return f'group {self.id}'

    def delete(self, using=None, keep_parents=False, soft=False, **kwargs):
        if soft:
            self.deleted_at = date.today()
            super().save()
        else:
            super().delete(using=None, keep_parents=False)


class TestGroupHistory(models.Model):

    class Actions(models.TextChoices):
        CREATED = 'Created'
        UPDATED = 'Updated'
        DELETED = 'Deleted'

    test_group = models.ForeignKey(TestGroup, on_delete=models.CASCADE, related_name='history')
    start_date = models.DateField()
    failure_modes = models.TextField()
    tests = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=7, choices=Actions.choices, default=Actions.UPDATED)

    def event_type(self):
        return self.event

