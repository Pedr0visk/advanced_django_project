from django.dispatch import receiver
from django.core import serializers

from .tasks import calc_results
from .signals import *


@receiver(schemas_compare_event)
def created_or_updated_schema(sender, instance, created, **kwargs):
    # getting user obj from request
    user = kwargs['user'].__dict__['_wrapped']
    user = serializers.serialize('json', [user, ])
    print('print user from campaign receivers', user)
    # calling celery to run this task in background
    calc_results.delay(instance.pk, user=user)
