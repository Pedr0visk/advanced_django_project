from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Campaign
from .forms import CampaignForm
from .filters import campaign_filter


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
def campaign_list(request):
    campaigns = Campaign.objects.order_by('-start_date')
    results = campaign_filter(campaigns, request.GET)
    context = {'campaigns': results}
    return render(request, 'campaigns/campaign_list.html', context)


@login_required
def campaign_create(request, bop_pk):
    form = CampaignForm()
    context = {'form': form, 'bop_pk': bop_pk}
    return render(request, 'campaigns/campaign_form.html', context)


def campaign_index(request, campaign_pk):
    campaign = Campaign.objects.prefetch_related('phases', 'events').get(pk=campaign_pk)
    context = {'campaign': campaign}
    return render(request, 'campaigns/campaign_index.html', context)
