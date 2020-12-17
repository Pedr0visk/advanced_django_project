from celery import shared_task

from . import metrics
from .models import Schema, Result
from .signals import *


@shared_task
def calc_results(schema_pk, *args, **kwargs):
    schema = Schema.objects.get(pk=schema_pk)
    values = metrics.run(schema)
    Result.objects.create(schema=schema, values=values)

    schemas_compare_calc_done.send(sender=Schema.__class__,
                                   user=kwargs['user'],
                                   instance=schema,
                                   created=True)
    return
