from django.contrib import messages
from django.core.exceptions import RequestAborted
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from .models import Bop, SafetyFunction
from .forms import BopForm, SafetyFunctionForm
from .load_bop import Loader as BopLoader
from .load_safety_function import Loader as SafetyFunctionLoader

from apps.csvs.models import Csv
from apps.managers.decorators import allowed_users
from ..failuremodes.models import FailureMode
from ..test_groups.models import TestGroup, TestGroupHistory, TestGroupDummy


@allowed_users(allowed_roles=['Admin'])
def upload(request):
    form = BopForm()
    context = {'form': form}

    if request.method == 'POST':
        form = BopForm(request.POST)
        bop = form.save()

        # remove file from database
        bopfile = Csv.objects.create(file_name=request.FILES['file'], bop=bop)

        BopLoader(bopfile.file_name.path, bop).run()

        messages.success(request, 'Bop created successfully')
        return redirect('list_bops')

    return render(request, 'bops/bop_form.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_list(request):
    bop_queryset = Bop.objects.all()
    context = {'bops': bop_queryset}
    return render(request, 'bops/bop_list.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_update(request, pk):
    bop = Bop.objects.get(pk=pk)
    form = BopForm(instance=bop)
    context = {'form': form}

    return render(request, 'bops/bop_form.html', context)


def index(request, pk):
    bop = Bop.objects.get(pk=pk)

    context = {'bop': bop}
    return render(request, 'bops/index.html', context)


@transaction.atomic
def safety_function_upload(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    form = SafetyFunctionForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            sf = form.save(commit=False)
            sf.bop = bop
            sf.save()

            cuts_txt = Csv.objects.create(file_name=request.FILES['file'], bop=bop)

            SafetyFunctionLoader(cuts_txt.file_name.path, safety_function=sf).run()
            return JsonResponse({'message': 'successfully created!'})

    context = {'bop': bop, 'form': form}
    return render(request, 'safety_functions/safety_function_form.html', context)


def safety_function_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf_set = bop.safety_functions.all()

    context = {'bop': bop, 'safety_functions': sf_set}
    return render(request, 'safety_functions/safety_function_list.html', context)


def safety_function_index(request, bop_pk, sf_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf = SafetyFunction.objects.get(pk=sf_pk)

    context = {'bop': bop, 'safety_function': sf}
    return render(request, 'safety_functions/index.html', context)


def safety_function_cuts(request, bop_pk, sf_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf = SafetyFunction.objects.get(pk=sf_pk)
    cut_set = sf.cuts.all()

    context = {'bop': bop, 'safety_function': sf, 'cuts': cut_set}
    return render(request, 'cuts/cut_list.html', context)


def test_planner(request, pk):
    bop = Bop.objects.get(pk=pk)
    test_group_set = TestGroup.objects.filter(bop=bop.pk, deleted_at__isnull=True).order_by('-updated_at')
    history = TestGroupHistory.objects.filter(test_group__bop_id__exact=bop.pk).order_by('-created_at')
    failure_modes_set = FailureMode.objects.filter(component__subsystem__bop__exact=bop,
                                                   testgroup__isnull=True)

    TestGroupDummy.objects.all().delete()
    for g in test_group_set:
        obj = TestGroupDummy(test_group=g,
                             start_date=g.start_date,
                             bop=bop,
                             tests=g.tests)
        obj.save()
        obj.failure_modes.set(g.failure_modes.all().values_list('id', flat=True))

    context = {
        'bop': bop,
        'test_groups': test_group_set,
        'history': history,
        'failure_modes': failure_modes_set
    }

    return render(request, 'bops/bop_test_planner.html', context)


def test_planner_raw(request, pk):
    bop = Bop.objects.get(pk=pk)
    test_group_set = TestGroupDummy.objects \
        .filter(bop=bop.pk, deleted_at__isnull=True) \
        .order_by('-updated_at')

    failure_modes_set = FailureMode.objects.filter(component__subsystem__bop__exact=bop,
                                                   testgroupdummy__isnull=True)
    print(failure_modes_set.count())
    context = {'bop': bop, 'test_groups': test_group_set, 'failure_modes': failure_modes_set}
    return render(request, 'bops/bop_test_planner.html', context)


def migrate(request, pk):
    bop = Bop.objects.get(pk=pk)

    try:
        TestGroup.objects.all().delete()
        test_group_set = TestGroupDummy.objects.all()
        for g in test_group_set:
            obj = TestGroup(start_date=g.start_date,
                            bop=bop,
                            tests=g.tests)
            obj.save()
            obj.failure_modes.set(g.failure_modes.all().values_list('id', flat=True))
    except RequestAborted:
        pass

    messages.success(request, 'Migrate Successfully!')
    return redirect('test_planner', pk)
