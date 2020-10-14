import json
import time
from apps.campaigns import metrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Campaign, Phase, Schema
from .forms import CampaignForm, PhaseForm
from .filters import campaign_filter

from django.shortcuts import get_object_or_404

from apps.test_groups.models import TestGroup


def campaign_update(request, campaign_pk):
    campaign = Campaign.objects.select_related('bop').get(pk=campaign_pk)

    form = CampaignForm(request.POST or None, instance=campaign)

    if request.method == 'POST':
        campaign = form.save()
        messages.success(request, 'Campaign updated successfully!')
        return redirect(campaign.success_url())

    context = {'form': form, 'bop_pk': campaign.bop.pk, 'campaign': campaign}
    return render(request, 'campaigns/campaign_form.html', context)


@login_required
def campaign_list(request):
    campaigns = Campaign.objects.order_by('-start_date')
    results = campaign_filter(campaigns, request.GET)
    context = {'campaigns': results}
    return render(request, 'campaigns/campaign_list.html', context)


@login_required
def campaign_create(request, bop_pk):
    form = CampaignForm(request.POST or None)

    if form.is_valid():
        campaign = form.save(commit=False)
        campaign.bop_id = bop_pk
        campaign.save()
        messages.success(request, f'Campaign "{campaign.name}" successfully created!')
        return redirect(campaign.success_url())

    context = {'form': form, 'bop_pk': bop_pk}
    return render(request, 'campaigns/campaign_form.html', context)


def campaign_index(request, campaign_pk):
    campaign = Campaign.objects.prefetch_related('schemas', 'events').get(pk=campaign_pk)
    context = {'campaign': campaign}
    return render(request, 'campaigns/campaign_index.html', context)


def phase_update(request, pk):
    phase = get_object_or_404(Phase, pk=pk)
    form = PhaseForm(request.POST or None, instance=phase)
    test_groups = TestGroup.objects.filter(bop_id=phase.campaign.bop.pk)
    if request.method == 'POST':
        if form.is_valid():
            p = form.save()
            if p.step == Phase.Step.TEST:
                try:
                    print(request.POST['test_groups'])
                    p.schedule.test_groups.set()
                except ModuleNotFoundError:
                    return
            return HttpResponse('updated!')

    context = {'phase': phase, 'form': form, 'test_groups': test_groups}
    return render(request, 'campaigns/phase_form.html', context)


def campaign_metrics(request, campaign_pk):
    campaign = Campaign.objects. \
        select_related('bop'). \
        prefetch_related('schemas').get(pk=campaign_pk)

    results = metrics.run(campaign)
    context = {'campaign': campaign, 'results': results}
    return HttpResponse(json.dumps(results))


def schema_create(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    context = {'campaign': campaign, 'campaign_pk': campaign_pk}
    return render(request, 'schemas/schema_form.html', context)


def schema_update(request, campaign_pk, schema_pk):
    schema = Schema.objects.prefetch_related('phases').get(pk=schema_pk)
    context = {'schema': schema, 'campaign_pk': campaign_pk}
    return render(request, 'schemas/schema_form.html', context)


def schema_index(request, campaign_pk, schema_pk):
    schema = Schema.objects.prefetch_related('phases', 'phases__test_groups').get(pk=schema_pk)

    context = {'schema': schema, 'campaign_pk': campaign_pk}
    return render(request, 'schemas/schema_index.html', context)


def schema_delete(request, campaign_pk, schema_pk):
    schema = Schema.objects.get(pk=schema_pk)
    schema.delete()
    messages.success(request, f'Schema "{schema.name}" deleted successfully')
    return redirect('campaigns:index', campaign_pk)
