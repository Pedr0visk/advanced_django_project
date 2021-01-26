from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification
from .signals import *


@receiver(task_initiated)
@receiver(task_completed)
def create_notification(sender, instance, *args, **kwargs):
    user = User.objects.get(pk=kwargs['user_id'])

    if kwargs['completed']:
        Notification.objects.create(
            assigned_to=user,
            group='d',
            body=f'Task completed! You can check the new results generated.',
            pk_relation=instance.pk
        )
    else:
        Notification.objects.create(
            assigned_to=user,
            group='c',
            body=f'A task has been created by user {user.username}, that may take a few seconds.',
            pk_relation=instance.pk
        )


@receiver(task_error)
def create_system_notification(sender, instance, *args, **kwargs):
    user = User.objects.get(pk=kwargs['user_id'])
    
    Notification.objects.create(
        assigned_to=user,
        group='s',
        body=kwargs['message'],
        pk_relation=None
    )


@receiver(post_save, sender=Notification)
def send_notification_info(*args, **kwargs):
    if kwargs['created']:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"campaign_group_{kwargs['instance'].assigned_to.id}", {
                'type': 'campaign_info',
                'group': kwargs['instance'].group,
                'body': kwargs['instance'].body
            }
        )
        async_to_sync(channel_layer.group_send)(
            f"notification_group_{kwargs['instance'].assigned_to.id}", {
                'type': 'notification_info'
            }
        )
