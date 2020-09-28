from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.bops.models import Bop
from .models import Campaign
from .forms import CampaignForm


def campaign_update(request, bop_pk, campaign_pk):
    bop = Bop.objects.get(pk=bop_pk)
    campaign = Campaign.objects.get(pk=campaign_pk)

    form = CampaignForm(request.POST or None, instance=campaign)

    if request.method == 'POST':
        campaign = form.save(commit=False)
        campaign.bop = bop
        campaign.save()

        messages.success(request, 'Campaign updated successfully!')
        return redirect('list_campaigns', bop_pk=bop_pk)

    context = {'form': form, 'bop': bop, 'campaign': campaign}
    return render(request, 'campaigns/campaign_form.html', context)


@login_required
def campaign_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    campaigns = bop.campaigns.all()

    context = {'bop': bop, 'campaigns': campaigns}
    return render(request, 'campaigns/campaign_list.html', context)


@login_required
def campaign_create(request, bop_pk):
    form = CampaignForm()
    bop = Bop.objects.get(pk=bop_pk)

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        campaign = form.save(commit=False)
        campaign.bop = bop
        campaign.save()
        print(request.POST.getlist['phases'])

        messages.success(request, 'Campaign created successfully')
        return redirect('list_campaigns', bop_pk=bop_pk)

    context = {'form': form, 'bop': bop}
    return render(request, 'campaigns/campaign_form.html', context)
