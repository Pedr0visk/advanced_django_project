from django.http.response import HttpResponse
from django.shortcuts import render

from apps.bops.models import Bop
from .models import Subsystem
from .filters import subsystem_filter


def subsystem_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    subsystems = subsystem_filter(request.GET)

    context = {'bop': bop, 'subsystems': subsystems}
    return render(request, 'subsystems/subsystem_list.html', context)


def index(request, bop_pk, slug):
    bop = Bop.objects.get(pk=bop_pk)
    subsystem = Subsystem.objects.get(slug=slug)

    context = {'bop': bop, 'subsystem': subsystem}
    return render(request, 'subsystems/index.html', context)
