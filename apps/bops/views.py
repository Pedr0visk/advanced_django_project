from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Bop, SafetyFunction, Component, FailureMode, Cut
from .forms import BopForm

from apps.campaigns.forms import CampaignForm


def upload(request):
    form = BopForm()

    if request.method == 'POST':
        file = request.POST['file']

    context = {'form': form}
    return render(request, 'bops/bop_form.html', context)


def campaign_list(request, pk):
    bop = Bop.objects.get(pk=pk)
    campaigns = bop.campaigns.all()

    context = {'bop': bop, 'campaigns': campaigns}
    return render(request, 'bops/campaign_list.html', context)


def campaign_create(request, pk):
    form = CampaignForm()

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        campaign = form.save(commit=False)
        campaign.bop = Bop.objects.get(pk=pk)
        campaign.save()

        messages.success(request, 'Campaign created successfully')
        return redirect('list_bop__campaigns', pk=pk)

    context = {'form': form}
    return render(request, 'bops/campaign_form.html', context)
