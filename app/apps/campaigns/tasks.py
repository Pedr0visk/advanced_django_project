from . import metrics
from .models import Schema, Result

from celery import shared_task


@shared_task
def calc_results(schema_pk):
    schema = Schema.objects.get(pk=schema_pk)
    print('schema name', schema)
    values = metrics.run(schema)
    print('results', values)
    Result.objects.create(schema=schema, values=values)
    return
