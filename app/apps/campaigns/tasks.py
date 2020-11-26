from celery import shared_task


@shared_task
def calc_results(schema):
    print(schema.name)
    return
