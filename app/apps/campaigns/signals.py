from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Campaign, Schema
from . import metrics


@receiver(post_save, sender=Schema)
def create_schema(sender, instance, created, **kwargs):
    if created:
        print('schema created')
        instance.results = metrics.run(instance)
        instance.save()
