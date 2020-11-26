from django.db.models.signals import post_save
from django.dispatch import receiver

from . import metrics
from .tasks import calc_results
from .models import Schema


@receiver(post_save, sender=Schema)
def created_or_updated_schema(sender, instance, created, **kwargs):
    calc_results.delay(instance.pk)
    return
