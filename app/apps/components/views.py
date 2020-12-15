from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ComponentForm
from .models import Component
from .filters import component_filter

from ..bops.models import Bop


def component_create(request):
    bop = request.GET.get('bop', '')
    form = ComponentForm(request.POST or None, bop=bop)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Subsystem successfully created!')
            return redirect('components:list')

    context = {'form': form}
    return render(request, 'components/component_form.html', context)


def component_update(request, component_pk):
    bop = request.GET.get('bop', '')
    component = Component.objects.get(pk=component_pk)
    form = ComponentForm(request.POST or None, instance=component, bop=bop)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Subsystem successfully updated!')
            return redirect('components:list')

    context = {'form': form}
    return render(request, 'components/component_form.html', context)


def component_delete(request, component_pk):
    component = Component.objects.get(pk=component_pk)

    if request.method == 'POST':
        component.delete()
        messages.success(request, 'Component deleted successfully!')
        return redirect('components:list')


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
