from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.utils import NestedObjects
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from datetime import timedelta

from ..bops.models import Bop
from ..test_groups.models import TestGroup


class Campaign(models.Model):
    class StatusCampaign(models.TextChoices):
        GREEN = 'Green'
        YELLOW = 'Yellow'
        ORANGE = 'Orange'
        RED = 'Red'

    name = models.CharField(max_length=100)
    bop = models.ForeignKey(
        Bop, on_delete=models.CASCADE, related_name='campaigns')
    active = models.BooleanField(default=False)
    well_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=6,
        choices=StatusCampaign.choices,
        default=StatusCampaign.GREEN
    )

    created = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def start_date(self):
        schema = self.schemas.filter(is_default=True).first()
        if schema:
            return schema.phases.first().start_date
        else:
            return None

    @property
    def end_date(self):
        schema = self.schemas.filter(is_default=True).first()
        if schema:
            start_date = schema.phases.latest('updated_at').start_date
            duration = schema.phases.latest('updated_at').duration
            end_date = start_date + timedelta(hours=duration)
            return end_date
        else:
            return None

    def get_period(self):
        """
        Get the campaign period converted in hours
        :return:
        """
        dt = self.end_date - self.start_date
        days = dt.days
        hours = days * 24
        return days, hours

    def get_schema_active(self):
        print('came here')
        return self.schemas.filter(is_default=True).first()

    def success_url(self):
        return reverse('campaigns:index', args=[self.pk])

    def get_absolute_url(self):
        return reverse('campaigns:index', args=[self.pk])

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(
            objs) for model, objs in collector.model_objs.items()}
        return model_count.items()

    def activate(self):
        self.active = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-active']


class Schema(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    cuts_contribution = models.TextField(blank=True, null=True)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 related_name='schemas')

    @property
    def start_date(self):
        return self.phases.first().start_date

    @property
    def end_date(self):
        start_date = self.phases.latest('updated_at').start_date
        duration = self.phases.latest('updated_at').duration
        end_date = start_date + timedelta(hours=duration)

        return end_date

    @property
    def last_result(self):
        return self.results.latest('created_at')

    @staticmethod
    def toggle_schema_default(schema):
        objects = Schema.objects.filter(campaign=schema.campaign, is_default=True).exclude(id=schema.id)

        for obj in objects:
            obj.is_default = False
            obj.save()

        print('saiu do for')
        objects = Schema.objects.filter(campaign=schema.campaign, is_default=True).exclude(id=schema.id)
        for obj in objects:
            print(obj.name, obj.is_default)

    def clean(self, *args, **kwargs):
        return super(Schema, self).save()

    def __str__(self):
        return self.name


class Phase(models.Model):
    name = models.CharField(max_length=255)
    schema = models.ForeignKey(Schema,
                               on_delete=models.CASCADE,
                               related_name='phases')

    test_groups = models.ManyToManyField(TestGroup)
    start_date = models.DateTimeField()
    duration = models.FloatField()
    has_test = models.BooleanField(default=False)
    is_drilling = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']


class Event(models.Model):
    class TypeEvent(models.TextChoices):
        COMP_REPAIR = 'CRIR', _('Repair in Component')
        SUBSYS_REPAIR = 'SRIR', _('Repair in Subsystem')
        COMP_REPLACE = 'CRCE', _('Replace in Component')
        SUBSYS_REPLACE = 'SRCE', _('Replace in Subsystem')
        WITHDRAW = 'WAW', _('Withdraw')
        REINSTALL = 'RLL', _('Reinstall')
        FMODE_FAIL = 'FIL', _('Failure in Failure Mode')
        COMP_FAIL = 'CIL', _('Failure in Component')
        SUBSYS_FAIL = 'SIL', _('Failure in Subsystem')

    description = models.TextField(blank=True, default='')
    object_code = models.CharField(blank=True, default='', max_length=255)
    created_by = models.ForeignKey(User,
                                   related_name='events_created',
                                   null=True,
                                   on_delete=models.SET_NULL)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='events')
    date = models.DateTimeField()

    type = models.CharField(
        max_length=14,
        choices=TypeEvent.choices,
        default=TypeEvent.WITHDRAW
    )

    def success_url(self):
        return reverse('campaigns:index', args=[self.campaign.pk])


    def __str__(self):
        return f'Event created by {self.created_by.username} at {self.date}'


class Result(models.Model):
    schema = models.ForeignKey(Schema,
                               on_delete=models.CASCADE,
                               related_name='results')

    values = models.TextField(blank=True, null=True)
    failures = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
