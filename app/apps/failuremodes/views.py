import json

from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import FailureMode
from .filters import failure_mode_filter
from .forms import FailureModeForm

# Don't forget to find a way to removed these
# classes bellow to reduce the acoplament
from apps.bops.models import Bop
from apps.subsystems.models import Subsystem
from apps.components.models import Component


def failuremode_list(request):
    bops = Bop.objects.order_by('name')
    subsystems = Subsystem.objects.order_by('name')
    components = Component.objects.order_by('name')
    dataset = failure_mode_filter(request.GET)

    context = {
        'dataset': dataset,
        'bops': bops,
        'subsystems': subsystems,
        'components': components
    }
    return render(request, 'failuremodes/failuremode_list.html', context)


def failuremode_create(request):
    bop = request.GET.get('bop', None)
    if bop is None:
        return redirect('failuremodes:list')

    form = FailureModeForm(request.POST or None)

    context = {'form': form}
    return render(request, 'failuremodes/failuremode_form.html', context)


def failuremode_update(request, fm_pk):
    failuremode = get_object_or_404(FailureMode, pk=fm_pk)
    form = FailureModeForm(request.POST or None, instance=failuremode)

    if request.method == 'POST':
        if form.is_valid():
            fm = form.save(commit=False)
            fm.distribution = FailureMode.format_distribution(fm.distribution)
            fm.save()
            return redirect('failuremodes:list')

    context = {'failuremode': failuremode, 'form': form}
    return render(request, 'failuremodes/failuremode_form.html', context)
