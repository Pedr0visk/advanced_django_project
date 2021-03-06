from django.dispatch import receiver
from django.core import serializers
from django.db.models.signals import post_save

from .models import Schema
from .tasks import *
from .signals import *


@receiver(schema_created_or_updated)
def on_schema_created_or_updated(sender, instance, created, **kwargs):
    user_id = kwargs['user_id']
    compare_schemas_for_campaign.delay(instance.pk, user_id=user_id)


@receiver(event_created)
def on_event_created(sender, instance, created, **kwargs):
    user_id = kwargs['user_id']
    create_result_for_schema_base.delay(instance.pk, user_id=user_id)


@receiver(post_save, sender=Schema)
def update_base_case_schema(sender, instance, **kwargs):
    if instance.is_default:
        Schema.toggle_schema_default(instance)
