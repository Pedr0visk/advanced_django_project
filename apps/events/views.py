from django.shortcuts import render
from django.core.cache import cache

from apps.bops.models import Bop


def event_list(request, bop_pk):
    bop = cache.get_or_set('bop', Bop.objects.get(pk=bop_pk))
    context = {'bop': bop}
    return render(request, 'events/event_list.html', context)
