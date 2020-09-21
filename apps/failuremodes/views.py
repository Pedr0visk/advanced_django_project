from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import FailureMode
from .filters import failuremode_filter
from .forms import FailureModeForm

from apps.bops.models import Bop


def failuremode_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    failuremodes = failuremode_filter(request.GET)

    context = {'bop': bop, 'failuremodes': failuremodes}
    return render(request, 'failuremodes/failuremode_list.html', context)


def failuremode_update(request, bop_pk, fm_pk):
    bop = Bop.objects.get(pk=bop_pk)
    failuremode = get_object_or_404(FailureMode, pk=fm_pk)
    form = FailureModeForm(request.POST or None, instance=failuremode)

    if request.method == 'POST':
        if form.is_valid():
            fm = form.save()
            return JsonResponse({'failuremode': model_to_dict(fm), 'message': 'successfully updated!'})

    context = {'bop': bop, 'failuremode': failuremode, 'form': form}
    return render(request, 'failuremodes/failuremode_form.html', context)
