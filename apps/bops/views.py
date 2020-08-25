from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bop, SafetyFunction, Component, FailureMode, Cut
from .forms import BopForm

from apps.campaigns.forms import CampaignForm


def upload(request):
    form = BopForm()
    context = {'form': form}
    return render(request, 'bops/bop_form.html', context)


@login_required
def campaign_list(request, pk):
    bop = Bop.objects.get(pk=pk)
    campaigns = bop.campaigns.all()

    context = {'bop': bop, 'campaigns': campaigns}
    return render(request, 'bops/campaign_list.html', context)


@login_required
def campaign_create(request, pk):
    form = CampaignForm()
    bop = Bop.objects.get(pk=pk)

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        campaign = form.save(commit=False)
        campaign.bop = bop
        campaign.save()

        messages.success(request, 'Campaign created successfully')
        return redirect('list_bop__campaigns', pk=pk)

    context = {'form': form, 'bop': bop}
    return render(request, 'bops/campaign_form.html', context)
