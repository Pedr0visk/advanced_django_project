from django.shortcuts import render
from .models import Bop, SafetyFunction, Component, FailureMode, Cut
from .forms import BopForm


def upload(request):
    form = BopForm()

    if request.method == 'POST':
        file = request.POST['file']


    context = {'form': form}
    return render(request, 'bops/bop_form.html', context)


def campaigns_list(request, pk):
    bop = Bop.objects.get(pk=pk)
    campaigns = bop.campaigns.all()

    context = {'bop': bop, 'campaigns': campaigns}
    return render(request, 'bops/campaign_list.html', context)

