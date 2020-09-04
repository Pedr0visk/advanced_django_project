import csv
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse

from .models import Bop, SafetyFunction
from .forms import BopForm, SafetyFunctionForm
from .load_bop import Loader as BopLoader
from .load_safety_function import Loader as SafetyFunctionLoader

from apps.csvs.models import Csv
from apps.managers.decorators import allowed_users


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


def safety_function_upload(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    form = SafetyFunctionForm()

    if request.method == 'POST':
        form = SafetyFunctionForm(request.POST)
        sf = form.save(commit=False)
        sf.bop = bop
        sf.save()

        cuts_txt = Csv.objects.create(file_name=request.FILES['file'], bop=bop)
        SafetyFunctionLoader(cuts_txt.file_name.path, safety_function=sf).run()

        messages.success(request, 'Safety Function created successfully!')
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

    context = {'bop': bop, 'safety_function': sf}
    return render(request, 'safety_functions/index.html', context)

def safety_function_cuts(request, bop_pk, sf_pk):
    bop = Bop.objects.get(pk=bop_pk)
    sf = SafetyFunction.objects.get(pk=sf_pk)
    cut_set = sf.cuts.all()

    context = {'bop': bop, 'safety_function': sf, 'cuts': cut_set}
    return render(request, 'cuts/cut_list.html', context)

def run(request, pk):
    campaign_period = 30 * 24
    """
        s1.reduce
    """
    sum_total = 0
    results = []
    for step in range(0, campaign_period, 24):
        # sum_total += s1.calculate_probability(step)
        results.append(sum_total)
        pass

    return HttpResponse('ok')
