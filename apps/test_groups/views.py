from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import TestGroupForm
from .models import TestGroup
from ..bops.models import Bop
from ..failuremodes.models import FailureMode
from ..tests.models import Test


def test_group_list(request):
    return HttpResponse('test group list')


def test_group_create(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    form = TestGroupForm(request.POST or None)
    test_set = Test.objects.all()
    failure_mode_set = FailureMode.objects.order_by('name').filter(component__subsystem__bop__exact=bop)

    if request.method == 'POST':
        if form.is_valid():
            tg = form.save(commit=False)
            tg.bop = bop
            tg.save()
            form.save_m2m()
            messages.success(request, 'Test Group created successfully!')
            return redirect('test_planner', bop_pk)

    context = {'form': form, 'bop': bop, 'tests': test_set, 'failure_modes': failure_mode_set}
    return render(request, 'test_groups/test_group_form.html', context)


def test_group_update(request, bop_pk, tg_pk):
    bop = Bop.objects.get(pk=bop_pk)
    test_group = TestGroup.objects.get(pk=tg_pk)
    failure_mode_set = FailureMode.objects.order_by('name').filter(component__subsystem__bop__exact=bop)
    form = TestGroupForm(request.POST or None, instance=test_group)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Test Group "{test_group}" updated successfully!')
            return redirect('test_planner', bop_pk)

    context = {'bop': bop, 'test_group': test_group, 'failure_modes': failure_mode_set, 'form': form}
    return render(request, 'test_groups/test_group_form.html', context)


def test_group_delete(request, bop_pk, tg_pk):
    bop = Bop.objects.get(pk=bop_pk)
    test_group = TestGroup.objects.get(pk=tg_pk)

    if request.method == 'POST':
        test_group_id = test_group.id
        test_group.delete()

        messages.success(request, f'Test Group "{test_group_id}" deleted successfully!')
        return redirect('test_planner', bop_pk)

    context = {'bop': bop, 'test_group': test_group}
    return render(request, 'test_groups/test_group_confirm_delete.html', context)
