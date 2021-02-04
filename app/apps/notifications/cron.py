from .models import Notification
from django.utils import timezone
from datetime import datetime, timedelta


def remove_older_notifications():
    """
    Remove notifications older then 15 days
    """
    expression = timezone.now() - timedelta(days=15)
    Notification.objects.filter(creation_date__lte=expression).delete()
