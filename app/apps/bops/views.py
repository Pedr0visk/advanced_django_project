from django.contrib import messages
from django.core.exceptions import RequestAborted
from django.db import transaction
from django.shortcuts import render, redirect

from .models import Bop, SafetyFunction
from .forms import BopForm, SafetyFunctionForm
from .load_bop import Loader as BopLoader
from .load_safety_function import Loader as SafetyFunctionLoader
from .decorators import query_debugger
from .signals import bop_created_or_updated

from ..certifications.forms import CertificationForm
from ..managers.decorators import allowed_users
from ..failuremodes.models import FailureMode



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
            new_bop = form.save()

            try:
                # load built-in bop
                BopLoader(new_bop).save_many(request.FILES['file'])
            except:
                pass

            # add latest certification
            if cert_form.is_valid():
                certification = cert_form.save(commit=False)
                certification.bop = new_bop
                certification.save()

            bop_created_or_updated.send(sender=Bop.__class__, instance=new_bop, created=True)
            messages.success(request, 'Bop created successfully')
            return redirect(new_bop.success_url())

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
            bop_created_or_updated.send(sender=Bop.__class__, instance=bop, created=False)
            messages.success(
                request, f'Successfully updated bop "{bop.name}" ')
            return redirect(bop.success_url())

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
        return redirect('dashboard')
    return render(request, 'bops/bop_confirm_delete.html', context)


def index(request, pk):
    bop = Bop.objects.prefetch_related('campaigns').get(pk=pk)
    request.session['bop_pk'] = bop.pk

    context = {'bop': bop}
    return render(request, 'bops/index.html', context)


def bop_hierarchy(request, pk):
    bop = Bop.objects.get(pk=pk)

    def serializer(failuremode):
        return {
            'id': failuremode.pk,
            'code': failuremode.code,
            'name': failuremode.name,
            'distribution': failuremode.distribution,
            'component': failuremode.component.name
        }

    failuremodes = [serializer(fm) for fm in bop.failure_modes]
    context = {'bop': bop, 'json_data': failuremodes}
    return render(request, 'bops/bop_hierarchy.html', context)


@query_debugger
def safety_function_index(request, bop_pk, sf_pk):
    sf = SafetyFunction.objects.prefetch_related('cuts').get(pk=sf_pk)
    bop = sf.bop
    cuts = list(sf.cuts.all().order_by('order').values(
        'id', 'failure_modes', 'order'))
    context = {'bop': bop, 'object': sf, 'json_data': cuts}
    return render(request, 'safety_functions/index.html', context)


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

            messages.success(
                request, f'Safety Function "{sf.name}" successfully created!')
            return redirect(sf.success_url())

    context = {'bop': bop, 'form': form}
    return render(request, 'safety_functions/safety_function_form.html', context)


def safety_function_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf_set = bop.safety_functions.all()

    context = {'bop': bop, 'safety_functions': sf_set}
    return render(request, 'safety_functions/safety_function_list.html', context)


def safety_function_update(request, bop_pk, sf_pk):
    sf = SafetyFunction.objects.select_related('bop').get(pk=sf_pk)
    form = SafetyFunctionForm(request.POST or None, instance=sf)
    context = {'object': sf, 'form': form}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Safety Function updated successfully!')
            return redirect('bops:index_safety_function', sf.bop.pk, sf.pk)
    return render(request, 'safety_functions/safety_function_form.html', context)


def safety_function_delete(request, bop_pk, sf_pk):
    sf = SafetyFunction.objects.select_related('bop').get(pk=sf_pk)

    if request.method == 'POST':
        sf_name = sf.name
        sf.delete()
        messages.success(
            request, f'Safety Function "{sf_name}" successfully deleted!')
        return redirect('bops:list_safety_functions', bop_pk)

    context = {'object': sf}
    return render(request, 'safety_functions/safety_function_confirm_delete.html', context)


def safety_function_cuts(request, bop_pk, sf_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf = SafetyFunction.objects.get(pk=sf_pk)
    cut_set = sf.cuts.all()

    context = {'bop': bop, 'safety_function': sf, 'cuts': cut_set}
    return render(request, 'cuts/cut_list.html', context)


def test_planner(request, pk):
    """
    Copy all tests groups to a mirror table called test groups dummy
    :param request:
    :param pk:
    :return:
    """
    bop = Bop.objects.prefetch_related(
        'testgroup', 'testgroupdummy').get(pk=pk)
    test_groups_set = bop.testgroup.order_by('-updated_at')
    failure_modes_set = FailureMode.objects.filter(component__subsystem__bop__exact=bop,
                                                   testgroup__isnull=True).order_by('code')

    bop.testgroupdummy.all().delete()

    for test_group in test_groups_set:
        new_test_group = bop.testgroupdummy.create(name=test_group.name,
                                                   test_group=test_group,
                                                   start_date=test_group.start_date,
                                                   tests=test_group.tests)
        new_test_group.failure_modes.set(
            test_group.failure_modes.all().values_list('id', flat=True))

    context = {
        'bop': bop,
        'test_groups': test_groups_set,
        'failure_modes': failure_modes_set
    }

    return render(request, 'bops/bop_test_planner.html', context)


def test_planner_raw(request, pk):
    bop = Bop.objects.prefetch_related(
        'testgroupdummy', 'testgroup').get(pk=pk)
    test_group_set = bop.testgroupdummy.order_by('-updated_at')

    failure_modes_set = FailureMode.objects.filter(component__subsystem__bop=bop,
                                                   testgroupdummy__isnull=True)

    if request.method == 'POST':
        try:
            bop.testgroup.all().delete()
            for dummy in test_group_set:
                new_test_group = bop.testgroup.create(name=dummy.name,
                                                      start_date=dummy.start_date,
                                                      tests=dummy.tests)
                new_test_group.failure_modes.set(
                    dummy.failure_modes.all().values_list('id', flat=True))
        except RequestAborted:
            raise RequestAborted

        messages.success(request, 'Migrate Successfully!')
        return redirect('bops:test_planner', pk)

    context = {'bop': bop, 'test_groups': test_group_set,
               'failure_modes': failure_modes_set}
    return render(request, 'bops/bop_test_planner.html', context)


def summary_results(request, pk):
    bop = Bop.objects.prefetch_related('safety_functions',
                                       'campaigns',
                                       'campaigns__phases').get(pk=pk)
    sf_pk = request.GET.get('sf')
    if sf_pk is not None:
        safety_function = bop.safety_functions.get(pk=sf_pk)
        metrics.run(bop, safety_function)
    context = {'bop': bop}
    return render(request, 'bops/summary_results.html', context)


def list_subsystems(request, pk):
    pass


def bop_result(request, pk):
    bop = Bop.objects.get(pk=pk)
    campaign = bop.active_campaign()
    schemas = campaign.schemas.all()

    context = {
        'bop': bop,
        'campaign': campaign,
        'schemas': schemas
    }

    return render(request, 'bops/bop_results.html', context)
