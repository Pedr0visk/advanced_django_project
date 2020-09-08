import csv
import time

from library import calc

from django.core.cache import cache

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse

from .models import Bop, SafetyFunction
from .forms import BopForm, SafetyFunctionForm
from .load_bop import Loader as BopLoader
from .load_safety_function import Loader as SafetyFunctionLoader

from apps.csvs.models import Csv
from apps.managers.decorators import allowed_users
from apps.failuremodes.models import FailureMode


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


def run(request, pk):
    start = time.perf_counter()

    b1 = Bop.objects.get(pk=pk)
    s1 = SafetyFunction.objects.first()
    step = 24

    fm_set = FailureMode.objects.all()

    # run all failure modes pfd by step
    # run cuts pfd for safety function

    cache.delete('failuremodes')

    if cache.get('failuremodes'):
        s1.pfd(step)
    else:
        data = {step: {}}

        for fm in FailureMode.objects.all():
            data[step][fm.code] = fm.pfd(step)

    s1.pfd(step)

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')

    return HttpResponse(fm_set.count())
