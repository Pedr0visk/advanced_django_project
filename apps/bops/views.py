import csv
from django.contrib import messages
from django.shortcuts import render, redirect


from .models import Bop, Test
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
