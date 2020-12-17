from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..campaigns.models import Result
from .models import Notification
from ..campaigns.signals import *


@receiver(schemas_compare_event)
@receiver(schemas_compare_calc_done)
def create_notification(*args, **kwargs):
    user = kwargs['user']

    if kwargs['created']:
        Notification.objects.create(
            assigned_to=user,
            group='d',
            body=f"Calculus is done!",
            pk_relation=user.id
        )
    else:
        Notification.objects.create(
            assigned_to=user,
            group='c',
            body=f"Hello {user.username}, we are doing some calculus, that take a few seconds.",
            pk_relation=user.id
        )


@receiver(post_save, sender=Notification)
def send_notification_info(*args, **kwargs):

    if kwargs['created']:
        channel_layer = get_channel_layer()

        print(kwargs['instance'].assigned_to.id)

        async_to_sync(channel_layer.group_send)(
            f"notification_group_{kwargs['instance'].assigned_to.id}", {
                'type': 'notification_info'
            }
        )
