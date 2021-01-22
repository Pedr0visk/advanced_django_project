from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import TestGroupDummyForm
from .models import TestGroupHistory, TestGroupDummy
from ..failuremodes.models import FailureMode
from ..tests.models import Test
from datetime import datetime, date as dt


def test_group_list(request):
    return HttpResponse('test group list')


def test_group_create(request, bop_pk):
    form = TestGroupDummyForm(request.POST or None, bop_pk=bop_pk)
    test_set = Test.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            fm_ids = request.POST.getlist('failure_modes')
            fm_set = FailureMode.objects.filter(component__subsystem__bop=bop_pk,
                                                testgroupdummy__isnull=False).values_list('id', flat=True)
            fm_set = list(dict.fromkeys(fm_set))
            date_set = list(TestGroupDummy.objects.filter(bop=bop_pk).values_list('start_date', flat=True))
            date = dt(*list(map(int, request.POST['start_date'].split('-'))))
            
            # need to put this blocks of code into clean class method
            count = 0
            for _id in fm_ids:
                if int(_id) in fm_set:
                    count += 1
                    break

            for d in date_set:
                if d == date:
                    count += 1
                    break

            if count == 2:
                messages.error(request,
                               'Another test group already exists with the same start date and same failure '
                               'mode(s)')
                return redirect('test_groups:create', bop_pk)

            tg = form.save(commit=False)
            tg.bop_id = bop_pk
            tg.save()
            form.save_m2m()
            messages.success(request, 'Test Group created successfully!')
            return redirect('bops:test_planner_raw', bop_pk)

    context = {'form': form, 'bop_pk': bop_pk, 'tests': test_set}
    return render(request, 'test_groups/test_group_form.html', context)


def test_group_update(request, tg_pk):
    test_group_raw = TestGroupDummy.objects.get(pk=tg_pk)
    form = TestGroupDummyForm(request.POST or None, instance=test_group_raw, bop_pk=test_group_raw.bop.pk)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Test Group "{test_group_raw}" updated successfully!')
            return test_group_raw.success_url()

    context = {'test_group': test_group_raw, 'form': form}
    return render(request, 'test_groups/test_group_form.html', context)


def test_group_delete(request, tg_pk):
    dummy = TestGroupDummy.objects.select_related('bop').get(pk=tg_pk)
    bop_pk = dummy.bop.pk

    if request.method == 'POST':
        test_group_id = dummy.id
        dummy.deleted_at = dt.today()
        dummy.save()

        messages.success(request, f'Test Group "{test_group_id}" deleted successfully!')
        return redirect('bops:test_planner_raw', bop_pk)

    context = {'test_group': dummy}
    return render(request, 'test_groups/test_group_confirm_delete.html', context)


def test_group_undo(request, bop_pk, history_pk):
    history = TestGroupHistory.objects.get(pk=history_pk)
    if history.event == 'Updated':
        test_group = history.test_group
        test_group.tests = history.tests
        test_group.start_date = history.start_date
        test_group.save()
        test_group.failure_modes.set([int(i) for i in history.failure_modes.split(',')])
        history.delete()

    if history.event == 'Created':
        test_group = history.test_group
        test_group.history.all().delete()
        test_group.delete()

    if history.event == 'Deleted':
        test_group = history.test_group
        test_group.deleted_at = None
        test_group.save()
        history.delete()

    messages.success(request, f'Undo changes on Test Group "{test_group}" successfully!')
    return redirect('test_planner', bop_pk)
