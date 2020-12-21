from django.dispatch import receiver
from django.core import serializers

from .tasks import calc_results
from .signals import *


@receiver(schemas_compare_event)
def created_or_updated_schema(sender, instance, created, **kwargs):
    user_id = kwargs['user_id']
    calc_results.delay(instance.pk, user_id=user_id)
