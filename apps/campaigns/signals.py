from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Campaign


@receiver(post_save, sender=Campaign)
def create_test_group(sender, instance, created, **kwargs):
    if created:
        instance.bop.schedule_tests()
