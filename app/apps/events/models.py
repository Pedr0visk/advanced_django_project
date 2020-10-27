from django.db import models
from django.urls import reverse

from apps.campaigns.models import Campaign
from django.utils.translation import gettext_lazy as _


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

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    object_code = models.CharField(blank=True, max_length=255)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='events')

    type = models.CharField(
        max_length=14,
        choices=TypeEvent.choices,
        default=TypeEvent.WITHDRAW
    )

    date = models.DateTimeField()

    def success_url(self):
        return reverse('campaigns:index', args=[self.campaign.pk])

    def __str__(self):
        return self.name
