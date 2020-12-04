from django.shortcuts import render

from apps.bops.models import Bop
from .models import Subsystem
from .filters import subsystem_filter


def subsystem_list(request):
    dataset = subsystem_filter(request.GET)
    bops = Bop.objects.order_by('name')
    context = {'dataset': dataset, 'bops': bops}
    return render(request, 'subsystems/subsystem_list.html', context)


def index(request, bop_pk, s_pk):
    bop = Bop.objects.get(pk=bop_pk)
    subsystem = Subsystem.objects.get(pk=s_pk)

    context = {'bop': bop, 'subsystem': subsystem}
    return render(request, 'subsystems/index.html', context)


def subsystem_components(request, bop_pk, slug):
    bop = Bop.objects.get(pk=bop_pk)
    subsystem = Subsystem.objects.get(slug=slug)
    components = subsystem.components.all()

    context = {'bop': bop, 'subsystem': subsystem, 'components': components}
    return render(request, 'subsystems/component_list.html', context)
