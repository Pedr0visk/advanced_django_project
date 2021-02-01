from celery import shared_task, Task

from . import metrics
from .models import Campaign, Result, Event

from ..notifications.signals import *

class LogErrorsTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_error.send(sender=Campaign.__class__, 
                        message='Error 500 - Internal error', 
                        instance=None,
                        user_id=kwargs['user_id'])     

        super(LogErrorsTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@shared_task(base=LogErrorsTask)
def compare_schemas_for_campaign(*args, **kwargs):
    """
    This function retrieves all the schemas of the selected campaign
    in order to loop throught them and calculate new results for 
    schema comparison
    """
    campaign = Campaign.objects.get(pk=kwargs['campaign_id'])

    # emit event to create a new notification of task initiated
    task_initiated.send(sender=Campaign.__class__,
                        completed=False,
                        instance=campaign,
                        user_id=kwargs['user_id'])

    for schema in campaign.schemas.all():
        values, failures = metrics.run(schema)
        Result.objects.create(schema=schema, values=values, failures=failures)

    # emit event to create a new notification of task completed
    task_completed.send(sender=Campaign.__class__,
                        completed=True,
                        instance=campaign,
                        user_id=kwargs['user_id'])

    bop = campaign.bop
    bop.results_updated()


@shared_task(base=LogErrorsTask)
def create_new_result_for_schema_base(*args, **kwargs):
    """
    Creates a new result for a single schema
    """
    campaign = Campaign.objects.get(pk=kwargs['campaign_id'])
    schema = campaign.get_schema_active()

    task_initiated.send(sender=Campaign.__class__,
                        completed=False,
                        instance=campaign,
                        user_id=kwargs['user_id'])

    values, failures = metrics.run(schema)
    Result.objects.create(schema=schema, values=values, failures=failures)

    
    task_completed.send(sender=Campaign.__class__,
                        completed=True,
                        instance=campaign,
                        user_id=kwargs['user_id'])

    bop = campaign.bop
    bop.results_updated()