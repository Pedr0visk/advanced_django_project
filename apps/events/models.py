from django.db import models
from django.urls import reverse

from apps.campaigns.models import Campaign
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    class TypeEvent(models.TextChoices):
        REPAIR = 'RIR', _('Repair')
        REPLACE = 'RCE', _('Replace')
        WITHDRAW = 'WAW', _('Withdraw')
        REINSTALL = 'RLL', _('Reinstall')
        COMP_FAIL = 'CIL', _('Failure in Component')
        FMODE_FAIL = 'FIL', _('Failure in Failure Mode')
        SUBSYS_FAIL = 'SIL', _('Failure in Subsystem')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='events')

    type = models.CharField(
        max_length=3,
        choices=TypeEvent.choices,
        default=TypeEvent.REPAIR
    )

    date = models.DateTimeField()

    def success_url(self):
        return reverse('campaigns:index', args=[self.campaign_id])

    def __str__(self):
        return self.name
