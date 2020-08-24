from django.shortcuts import render, redirect
from django.contrib import messages

from apps.bops.models import Bop
from .models import Campaign
from .forms import CampaignForm


def campaign_update(request, bop_pk, campaign_pk):
    bop = Bop.objects.get(pk=bop_pk)
    campaign = Campaign.objects.get(pk=campaign_pk)

    form = CampaignForm(instance=campaign)

    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        campaign = form.save(commit=False)
        campaign.bop = bop
        campaign.save()

        messages.success(request, 'Campaign updated successfully!')
        return redirect('list_bop__campaigns', pk=bop_pk)

    context = {'form': form, 'bop': bop}
    return render(request, 'campaigns/campaign_form.html', context)
