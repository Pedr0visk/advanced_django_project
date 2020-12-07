from django.contrib import messages
from django.shortcuts import render, redirect
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
    bop = request.GET.get('bop', '')
    form = SubsystemForm(request.POST or None, bop=bop)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Subsystem successfully added!')

            return redirect('%s?bop=%s' % (reverse('subsystems:list'), bop))

    context = {'form': form}
    return render(request, 'subsystems/subsystem_form.html', context)


def subsystem_update(request, subsystem_pk):
    bop = request.GET.get('bop', '')
    subsystem = Subsystem.objects.get(pk=subsystem_pk)
    form = SubsystemForm(request.POST or None, instance=subsystem, bop=bop)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Subsystem successfully updated!')

            return redirect('%s?bop=%s' % (reverse('subsystems:list'), bop))

    context = {'form': form}
    return render(request, 'subsystems/subsystem_form.html', context)


def subsystem_delete(request, subsystem_pk):
    bop = request.GET.get('bop', '')
    subsystem = Subsystem.objects.get(pk=subsystem_pk)

    if request.method == 'POST':
        subsystem.delete()
        messages.success(request, 'Subsystem successfully deleted!')
        return redirect('%s?bop=%s' % (reverse('subsystems:list'), bop))


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
