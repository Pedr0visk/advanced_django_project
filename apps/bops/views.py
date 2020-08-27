import csv
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.managers.decorators import allowed_users

from .models import Bop, Subsystem, Component, FailureMode, Test
from .forms import BopForm
from apps.csvs.models import Csv


@allowed_users(allowed_roles=['Admin'])
def upload(request):
    form = BopForm()
    context = {'form': form}

    if request.method == 'POST':
        form = BopForm(request.POST)
        bop = form.save()

        # remove file from database
        bopfile = Csv.objects.create(file_name=request.FILES['file'], bop=bop)

        # Loop through bopfile.txt and save in chunks
        with open(bopfile.file_name.path) as csvfile:

            # read file from line 1
            infile = csv.reader(csvfile, delimiter=',')
            rows = [line for line in infile][1:]

            for row in rows:
                s, created = Subsystem.objects.get_or_create(code=row[2], name=row[1], bop=bop)
                c, created = Component.objects.get_or_create(code=row[4], name=row[3], subsystem=s)
                f, created = FailureMode.objects.get_or_create(code=row[7],
                                                               name=row[5],
                                                               diagnostic_coverage=get_column(row, 11),
                                                               component=c)
                t1, created = Test.objects.get_or_create(interval=get_column(row, 9), coverage=get_column(row, 14))
                t2, created = Test.objects.get_or_create(interval=get_column(row, 10), coverage=get_column(row, 15))
                t3, created = Test.objects.get_or_create(interval=get_column(row, 11), coverage=get_column(row, 16))
                t4, created = Test.objects.get_or_create(interval=get_column(row, 12), coverage=get_column(row, 17))

        messages.success(request, 'Bop created successfully')
        return redirect('list_bops')

    return render(request, 'bops/bop_form.html', context)


@allowed_users(allowed_roles=['Admin'])
def bop_list(request):
    bop_queryset = Bop.objects.all()
    context = {'bops': bop_queryset}
    return render(request, 'bops/bop_list.html', context)


def get_column(row, index):
    """
    if column is blank return 1
    """
    if row[index] is None or row[index] == '':
        return 1
    else:
        return row[index]
