from celery import shared_task

from . import metrics
from .models import Campaign, Result

from ..notifications.signals import *


@shared_task
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

    try:
        # initing calc results and calling schema compare
        for schema in campaign.schemas.all():
            values, failures = metrics.run(schema)
            Result.objects.create(schema=schema, values=values, failures=failures)
    except RuntimeError:
        print('catching error')
        system_error.send(sender=Campaign.__class__,
                          completed=True,
                          instance=campaign,
                          user_id=kwargs['user_id'])
        return

    # emit event to create a new notification of task completed
    task_completed.send(sender=Campaign.__class__,
                        completed=True,
                        instance=campaign,
                        user_id=kwargs['user_id'])


@shared_task
def create_new_result_for_schema_base(*args, **kwargs):
    """
    Creates a new result for a single schema
    """
    print('creating new result for schema')
    campaign = Campaign.objects.get(pk=kwargs['campaign_id'])
    schema = campaign.get_schema_active()

    task_initiated.send(sender=Campaign.__class__,
                        completed=False,
                        instance=campaign,
                        user_id=kwargs['user_id'])

    try:
        values, failures = metrics.run(schema)
        Result.objects.create(schema=schema, values=values, failures=failures)
    except:
        system_error.send(sender=Campaign.__class__,
                          completed=True,
                          instance=campaign,
                          user_id=kwargs['user_id'])
        return
    
    task_completed.send(sender=Campaign.__class__,
                        completed=True,
                        instance=campaign,
                        user_id=kwargs['user_id'])
