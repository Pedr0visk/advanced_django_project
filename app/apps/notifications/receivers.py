from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification
from .signals import *


@receiver(task_initiated)
@receiver(task_completed)
def create_notification(sender, *args, **kwargs):
    user = User.objects.get(pk=kwargs['user_id'])

    if kwargs['completed']:
        Notification.objects.create(
            assigned_to=user,
            group='d',
            body='Task initiated',
            pk_relation=user.id
        )
    else:
        Notification.objects.create(
            assigned_to=user,
            group='c',
            body='Task completed',
            pk_relation=user.id
        )


@receiver(post_save, sender=Notification)
def send_notification_info(*args, **kwargs):

    if kwargs['created']:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notification_group_{kwargs['instance'].assigned_to.id}", {
                'type': 'notification_info'
            }
        )
