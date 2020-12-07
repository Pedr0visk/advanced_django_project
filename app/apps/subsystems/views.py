from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse

from apps.bops.models import Bop

from .forms import SubsystemForm
from .models import Subsystem
from .filters import subsystem_filter


def subsystem_list(request):
    dataset = subsystem_filter(request.GET)
    bops = Bop.objects.order_by('name')
    context = {'dataset': dataset, 'bops': bops}
    return render(request, 'subsystems/subsystem_list.html', context)


def subsystem_create(request):
    form = SubsystemForm(request.POST or None, query_params=request.GET)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return '%s?bop%s' % (reverse('subsystems:list'), bop.id)

    context = {'form': form}
    return render(request, 'subsystems/subsystem_form.html', context)


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
