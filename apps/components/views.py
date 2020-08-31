from django.shortcuts import render

from .models import Component
from .filters import component_filter
from apps.bops.models import Bop


def component_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    components = component_filter(request.GET)

    context = {'bop': bop, 'components': components}
    return render(request, 'components/component_list.html', context)
