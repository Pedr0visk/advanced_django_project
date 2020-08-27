import csv
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Bop, Subsystem, Component, FailureMode, Test
from .forms import BopForm
from .load import Loader

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

        Loader(bopfile.file_name.path, bop).run()

        messages.success(request, 'Bop created successfully')
        return redirect('list_bops')

    return render(request, 'bops/bop_form.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_list(request):
    bop_queryset = Bop.objects.all()
    context = {'bops': bop_queryset}
    return render(request, 'bops/bop_list.html', context)


def bop_update(request, pk):
    fm = FailureMode.objects.get(pk=1430)
    return HttpResponse(fm.distribution['cycle']['limit'])


def get_distribution(row):
    distribution = {'type': row[22]}

    if row[22] == 'Exponential':
        distribution['exponential_failure_rate'] = row[23]

    elif row[22] == 'Probability':
        distribution['probability'] = get_column(row, 23)

    elif row[22] == 'Weibull':
        distribution['scale'] = row[24]
        distribution['form'] = row[25]

    elif row[22] == 'Step':
        distribution['cycle'] = {}
        distribution['inital_failure_rate'] = row[26]
        distribution['cycle']['value'] = int(row[27]) / 100
        distribution['cycle']['limit'] = row[28]
        distribution['cycle']['size'] = row[29]

    return distribution


def get_column(row, index):
    """
    if column is blank return 1
    """
    if row[index] is None or row[index] == '':
        return 1
    else:
        return row[index]
