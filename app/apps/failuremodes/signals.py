from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import FailureMode


@receiver(post_save, sender=FailureMode)
def on_failuremode_created_or_updated(sender, instance, created, **kwargs):
    bop = instance.component.subsystem.bop
    bop.is_outdated = True
    bop.save()
