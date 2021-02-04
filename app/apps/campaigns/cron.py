from .models import Campaign
from django.utils import timezone


def check_active_campaigns():
    print('***** running cron *******')
    for campaign in Campaign.objects.filter(created=True, active=False).all():
        if campaign.start_date <= timezone.now():
            campaign.activate()
