from django.core.management.base import BaseCommand, CommandError
from ...models import Campaign
from django.utils import timezone


class Command(BaseCommand):
    help = 'Activate campaigns'

    def handle(self, *args, **options):
        for campaign in Campaign.objects.filter(created=True, active=False):
            if campaign.start.date > timezone.now():
                campaign.activate()

        self.stdout.write(self.style.SUCCESS('Campaigns activated successfully!'))
