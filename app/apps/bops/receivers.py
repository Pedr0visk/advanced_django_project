from django.dispatch import receiver
from .signals import *
from .models import Bop


@receiver(bop_created_or_updated)
def generate_matrix_on_bop_created(sender, **kwargs):
    instance = kwargs['instance']
    instance.matrix = Bop.get_matrix(instance)
    instance.save()

    return
