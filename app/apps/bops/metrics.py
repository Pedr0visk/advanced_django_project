from apps.failuremodes.models import FailureMode


def run(bop, safety_function):
    campaigns_set = bop.campaigns.all()
    failure_modes_set = FailureMode.objects.filter(component__subsystem__bop=bop)
    cuts_set = safety_function.cuts.all()
    results = []
    table_fm_results = []

    table_fm_results = init_table(table_fm_results, campaigns_set)
    table_fm_results = fill_table(table_fm_results, failure_modes_set)


def init_table(table, campaigns):
    for c in campaigns:
        days, hours = c.get_period()


    return []


def fill_table(table, failure_modes):
    return 1


def get_campaign_result(campaign):
    period = campaign.end_date - campaign.start_date
    phases = campaign.phases.all()

    if phases is None:
        return

    for phase in phases:
        if phase.step == phase.Step.TEST:
            return
    pass
