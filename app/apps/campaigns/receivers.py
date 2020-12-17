from django.db.models.signals import post_save
from django.dispatch import receiver

from . import metrics
from .tasks import calc_results
from .signals import *
from .models import Schema, Result


@receiver(schemas_compare_event)
def created_or_updated_schema(sender, instance, created, **kwargs):
    print('initing calc')
    calc_results(instance.pk, user=kwargs['user'])
    print('end calc')
