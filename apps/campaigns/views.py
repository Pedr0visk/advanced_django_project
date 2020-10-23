import json
import time
from . import metrics
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


def campaign_metrics(request, schema_pk):
    schema = Schema.objects.get(pk=schema_pk)
    campaign = schema.campaign
    results = metrics.run(schema)
    schema.result = results
    schema.save()

    time = []
    number_Sf = len(results[0])
    tempo = len(results) - 1
    data_to_charts = []

    print("veiws number sf", number_Sf, tempo)

    for j in range(1, number_Sf):
        result_sf = []
        average_to_chart = []
        # result_sf_falho = []
        soma = 0
        avg = 0
        for i in range(1, tempo):
            if j == 1:
                time.append(results[i][0])

            result_sf.append(results[i][j])
            soma = soma + results[i][j]
            # if i+2 > inicio:
            #    result_sf_falho.append(result_falho[i][j])
            # else:
            #    result_sf_falho.append("null")

        avg = soma / tempo

        maximo = max(result_sf)

        desc = "safety Function" + " " + str(j)

        for i in range(0, tempo):
            average_to_chart.append(avg)
        print("a", average_to_chart)
        print("desc", desc, soma, tempo)
        data_to_charts.append({
            'average': avg,
            'average_to_chart': average_to_chart,
            'result': result_sf,
            'max': maximo,
            'desc': desc,
        })

    context = {'campaign': campaign, 'schema': Schema, 'results': results, 'data_to_charts': data_to_charts}
    return render(request, 'campaigns/campaign_charts.html', context)


def campaign_delete(request, campaign_pk):
    campaign = Campaign.objects.select_related('bop').get(pk=campaign_pk)
    context = {'object': campaign}

    if request.method == 'POST':
        name = campaign.name
        bop = campaign.bop
        campaign.delete()
        messages.success(request, f'Bop "{name}" successfully deleted')
        return redirect('bops:index', bop.pk)

    return render(request, 'campaigns/campaign_confirm_delete.html', context)


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
