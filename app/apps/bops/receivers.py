from django.dispatch import receiver
from .signals import *
from .models import Bop


@receiver(bop_created)
def generate_matrix_on_bop_created(sender, **kwargs):
    created = kwargs['created']
    instance = kwargs['instance']

    if created:
        instance.matrix = Bop.get_matrix(instance)
        instance.save

    return
