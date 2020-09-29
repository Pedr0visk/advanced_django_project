from django.contrib import messages
from django.core.exceptions import RequestAborted
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.cache import cache

from .models import Bop, SafetyFunction
from .forms import BopForm, SafetyFunctionForm
from .load_bop import Loader as BopLoader
from .load_safety_function import Loader as SafetyFunctionLoader

from apps.certifications.forms import CertificationForm

from apps.managers.decorators import allowed_users
from ..failuremodes.models import FailureMode
from ..test_groups.models import TestGroup, TestGroupDummy


@transaction.atomic
@allowed_users(allowed_roles=['Admin'])
def bop_upload(request):
    """
    Add a new bop from a built-in bop.text
    :param request:
    :return:
    """
    form = BopForm(request.POST or None, request.FILES or None)
    cert_form = CertificationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            bop = form.save()

            # load built-in bop
            BopLoader(bop).save_many(request.FILES['file'])

            # add latest certification
            if cert_form.is_valid():
                certification = cert_form.save(commit=False)
                certification.bop = bop
                certification.save()

            messages.success(request, 'Bop created successfully')
            return redirect('list_bops')

    context = {'form': form, 'cert_form': cert_form}
    return render(request, 'bops/bop_form.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_list(request):
    bop_queryset = Bop.objects.all()
    context = {'bops': bop_queryset}
    return render(request, 'bops/bop_list.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_update(request, pk):
    bop = Bop.objects.get(pk=pk)
    form = BopForm(request.POST or None, instance=bop)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated bop "{bop.name}" ')
            return redirect('index_bop', bop.pk)

    context = {'form': form, 'bop': bop}
    return render(request, 'bops/bop_form.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_delete(request, pk):
    bop = Bop.objects.get(pk=pk)
    context = {'bop': bop}

    if request.method == 'POST':
        name = bop.name
        bop.delete()
        messages.success(request, f'Bop "{name}" successfully deleted')
        return redirect('list_bops')
    return render(request, 'bops/bop_confirm_delete.html', context)


def index(request, pk):
    bop = Bop.objects.get(pk=pk)
    cache.set('bop', bop)

    context = {'bop': bop}
    return render(request, 'bops/index.html', context)


@transaction.atomic
def safety_function_upload(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    form = SafetyFunctionForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            sf = form.save(commit=False)
            sf.bop = bop
            sf.save()

            SafetyFunctionLoader(request.FILES['file'], sf).run()

            messages.success(request, f'Safety Function "{sf.name}" successfully created!')
            return redirect('list_safety_functions', bop.pk)

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

    context = {'bop': bop, 'object': sf}
    return render(request, 'safety_functions/index.html', context)


def safety_function_delete(request, bop_pk, sf_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf = SafetyFunction.objects.get(pk=sf_pk)

    if request.method == 'POST':
        sf_name = sf.name
        sf.delete()
        messages.success(request, f'Safety Function "{sf_name}" successfully deleted!')
        return redirect('list_safety_functions', bop_pk)

    context = {'bop': bop, 'object': sf}
    return render(request, 'safety_functions/safety_function_confirm_delete.html', context)


def safety_function_cuts(request, bop_pk, sf_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf = SafetyFunction.objects.get(pk=sf_pk)
    cut_set = sf.cuts.all()

    context = {'bop': bop, 'safety_function': sf, 'cuts': cut_set}
    return render(request, 'cuts/cut_list.html', context)


def test_planner(request, pk):
    bop = Bop.objects.get(pk=pk)
    test_group_set = TestGroup.objects.filter(bop=bop.pk, deleted_at__isnull=True).order_by('-updated_at')
    failure_modes_set = FailureMode.objects.filter(component__subsystem__bop__exact=bop,
                                                   testgroup__isnull=True).order_by('code')

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
