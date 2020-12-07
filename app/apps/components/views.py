from django.shortcuts import render

from .models import Component
from .filters import component_filter
from apps.bops.models import Bop


def component_list(request):
    bops = Bop.objects.order_by('name')
    dataset = component_filter(request.GET)

    context = {'dataset': dataset, 'bops': bops}
    return render(request, 'components/component_list.html', context)


def index(request, bop_pk, c_pk):
    bop = Bop.objects.get(pk=bop_pk)
    component = Component.objects.get(pk=c_pk)

    context = {'bop': bop, 'component': component}
    return render(request, 'components/index.html', context)
