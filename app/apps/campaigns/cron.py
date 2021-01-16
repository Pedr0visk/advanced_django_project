from .models import Campaign
from django.utils import timezone


def activate_campaigns():
    for campaign in Campaign.objects.filter(created=True, active=False):
        if campaign.start_date <= timezone.now():
            print('activating campaign', campaign.name)
            campaign.activate()

