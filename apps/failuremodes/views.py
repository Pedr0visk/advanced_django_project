from django.shortcuts import render
from .models import FailureMode
from .filters import failuremode_filter

from apps.bops.models import Bop


def failuremode_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    failuremodes = failuremode_filter(request.GET)

    context = {'bop': bop, 'failuremodes': failuremodes}
    return render(request, 'failuremodes/failuremode_list.html', context)


def index(request, bop_pk, slug):
    bop = Bop.objects.get(pk=bop_pk)
    failuremode = FailureMode.objects.get(slug=slug)

    context = {'bop': bop, 'failuremode': failuremode}
    return render(request, 'subsystems/index.html', context)
