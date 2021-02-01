from django.dispatch import receiver
from django.core import serializers
from django.db.models.signals import post_save

from .models import Schema, Phase
from .tasks import *
from .signals import *


@receiver(schema_created_or_updated)
def on_schema_created_or_updated(sender, instance, created, **kwargs):
    user_id = kwargs['user_id']
    compare_schemas_for_campaign.delay(instance.pk, user_id=user_id)


@receiver(post_save, sender=Schema)
def update_base_case_schema(sender, instance, **kwargs):
    if instance.is_default:
        Schema.toggle_schema_default(instance)

@receiver(post_save, sender=Phase)
def outdate_bop_on_phase_created_or_updated(sender, instance, **kwargs):
    schema = instance.schema
    
    if schema.is_default:
        bop = schema.campaign.bop
        bop.is_outdated = True
        bop.save()

@receiver(post_save, sender=Event)
def outdate_bop_on_phase_created_or_updated(sender, instance, **kwargs):
    bop = instance.campaign.bop
    bop.is_outdated = True
    bop.save()
    
        

