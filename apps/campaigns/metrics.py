from apps.failuremodes.models import FailureMode
from apps.campaigns.models import Campaign, Phase
from apps.failuremodes.models import FailureMode

def run(bop):
    campaigns = bop.campaigns
    failure_mode_set = FailureMode.objects.filter(component__subsystem__bop=bop)
    test_groups = bop.testgroup.all()

    sfs = bop.safety_functions.all()
    for sf in sfs:
        cuts = sf.cuts.all()

    failure_modes = FailureMode.objects.filter(component__subsystem__bop__exact=bop)

    return
