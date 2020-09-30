from apps.failuremodes.models import FailureMode
from apps.campaigns.models import Campaign, Phase


def run(campaign):
    bop = campaign.bop
    sfs = bop.safety_functions.all()
    for sf in sfs:
        cuts = sf.cuts.all()

    jobs = campaign.jobs

    phases = campaign.phases.all()
    events = campaign.event_set.all()

    failure_modes = FailureMode.objects.filter(component__subsystem__bop__exact=bop)

    return
