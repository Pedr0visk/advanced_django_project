import ast
import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from apps.bops.models import *
from apps.cuts.models import *
from .metrics import *
from .models import Campaign, Phase, Schema, Event, Result
from .forms import CampaignForm, PhaseForm, EventForm
from .filters import campaign_filter
from .tasks import *
from ..test_groups.models import TestGroup


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
        messages.success(
            request, f'Campaign "{campaign.name}" successfully created!')
        return redirect(campaign.success_url())

    context = {'form': form, 'bop_pk': bop_pk}
    return render(request, 'campaigns/campaign_form.html', context)


def campaign_index(request, campaign_pk):
    campaign = Campaign.objects.prefetch_related(
        'schemas', 'events').get(pk=campaign_pk)

    # activate campaign and set a base schema
    if request.method == 'POST':
        schema = Schema.objects.get(pk=request.POST.get('id_schema'))
        schema.is_default = True
        schema.save()

        # activating campaign temporaly here
        # cause we need to have access to the dashboard
        campaign.active = True
        campaign.save()

        messages.success(
            request, f'Schema "{schema.name}" has been choosen for the f{campaign.name}')

    context = {'campaign': campaign, 'bop': campaign.bop}

    if campaign.active:
        return render(request, 'campaigns/campaign_index.html', context)

    return render(request, 'campaigns/campaign_planner.html', context)


def campaign_planner(request, campaign_pk):
    campaign = Campaign.objects.prefetch_related('schemas').get(pk=campaign_pk)
    context = {'campaign': campaign, 'bop': campaign.bop}
    return render(request, 'campaigns/campaign_planner.html', context)


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
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    schema = campaign.get_schema_active()
    safety_functions = campaign.bop.safety_functions.all()
    #results = ast.literal_eval(schema.last_result.values)
    #result_falho = ast.literal_eval(schema.last_result.failures)
    today = metrics.actual_step(schema)
    campaign = schema.campaign

    results, result_falho = metrics.run(schema)


    number_Sf = len(results[0])
    tempo = len(results) - 1
    data_to_charts = []
    data_to_table = []
    average = []
    list_max = []
    list_fail_max = []
    inicio = len(results) - 1
    f = 0

    fail_events = Event.objects.filter(campaign=schema.campaign)

    for fail in fail_events:
        if f == 0:
            tempo_falha = fail.date
            tempo_falha = tempo_falha.replace(tzinfo=None)

            inicio = (tempo_falha - schema.start_date.replace(tzinfo=None))
            inicio = int(inicio.total_seconds() / 60 ** 2)
            f = 1
    j = 0
    for sf in safety_functions:
        j = j + 1

        result_sf = []
        result_sf_falho = []
        result_sf_to_chart = []
        average_to_chart = []
        today_result = []

        soma_total = 0
        soma_no_fail = 0
        peso = 0
        td = 0
        for i in range(0, tempo):
            result_sf.append(results[i][j])
            if i + 2 > inicio and inicio != tempo:
                if results[inicio + 2][j] == result_falho[inicio + 2][j]:
                    result_sf_falho.append(0)
                else:
                    result_sf_falho.append(result_falho[i][j])
            else:
                result_sf_falho.append(0)

            if i + 1 > today:

                soma_no_fail = soma_no_fail + result_sf[i]

                if i + 1 > inicio and result_sf_falho[i] != 0:
                    peso = peso + 1
                    soma_total = soma_total + result_sf_falho[i]
                else:
                    soma_total = soma_total + result_sf[i]

        avg = soma_total / (tempo - today)
        avg_no_fail = soma_no_fail / (tempo - today)
        print("peso", peso, (tempo - today))
        print("avg", avg, avg_no_fail)
        average.append(avg)

        list_max.append(max(result_sf))

        if max(result_sf_falho):
            list_fail_max.append(max(result_sf_falho))
        else:
            list_fail_max.append(0)

        desc =  sf.name
        cont = 0

        result_teste_sf = []

        phases = schema.phases.all().order_by('start_date')

        for phase in phases:
            if phase.has_test:
                for i in range(0, int(phase.duration)):
                    result_teste_sf.append(result_sf[cont])
                    result_sf_to_chart.append(0)
                    cont = cont + 1
                if result_sf[cont]:
                    result_teste_sf.append(result_sf[cont])
            else:
                for i in range(0, int(phase.duration)):
                    result_teste_sf.append(0)
                    result_sf_to_chart.append(result_sf[cont])
                    cont = cont + 1

        for i in range(0, tempo):
            if i == today:
                today_result.append(result_sf[i])
                today_result.append(avg)
                td = result_sf[i]
            else:
                today_result.append(0)

            if i > today:
                average_to_chart.append(avg)
            else:
                average_to_chart.append('Null')

        data_to_charts.append({
            'average_to_chart': average_to_chart,
            'result_teste_sf': result_teste_sf,
            'result': result_sf_to_chart,
            'result_sf_falho': result_sf_falho,
            'desc': desc,
            'today_result': today_result
        })

        data_to_table.append({
            'safety_function': sf,
            'today': td,
            'average_fail': avg_no_fail,
            'average': avg,
            'max': max(result_sf)
        })

    start_date = campaign.start_date.replace(tzinfo=None)

    context = {
        'campaign': campaign,
        'start_date':start_date,
        'schema': schema,
        'average': average,
        'maxi': list_max,
        'maxi_fail': list_fail_max,
        'data_to_charts': data_to_charts,
        'data_to_table':data_to_table,
        'today': td,
    }

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


def campaign_run(request, campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    safety_functions = campaign.bop.safety_functions.all()
    schema = campaign.get_schema_active()
    today = metrics.actual_step(schema)
    
    if schema.last_result is None:
        messages.error(request, 'There is no results created on database.')
        return redirect('campaigns:index', campaign.pk)

    results = ast.literal_eval(schema.last_result.values)
    result_falho = ast.literal_eval(schema.last_result.failures)

    number_Sf = len(results[0])
    tempo = len(results) - 1
    data_to_charts = []
    data_to_table = []
    average = []
    list_max = []
    list_fail_max = []
    inicio = len(results) - 1
    f = 0

    fail_events = Event.objects.filter(campaign=schema.campaign)

    for fail in fail_events:
        if f == 0:
            tempo_falha = fail.date
            tempo_falha = tempo_falha.replace(tzinfo=None)

            inicio = (tempo_falha - schema.start_date.replace(tzinfo=None))
            inicio = int(inicio.total_seconds() / 60 ** 2)
            f = 1
    j = 0
    for sf in safety_functions:
        j = j + 1

        result_sf = []
        result_sf_falho = []
        result_sf_to_chart = []
        average_to_chart = []
        today_result = []

        soma_total = 0
        soma_no_fail = 0
        peso = 0
        for i in range(0, tempo):
            result_sf.append(results[i][j])
            if i + 2 > inicio and inicio != tempo:
                if results[inicio + 2][j] == result_falho[inicio + 2][j]:
                    result_sf_falho.append(0)
                else:
                    result_sf_falho.append(result_falho[i][j])
            else:
                result_sf_falho.append(0)

            if i + 1 > today:
                peso = peso + 1
                soma_no_fail = soma_no_fail + result_sf[i]

                if i + 1 > inicio and result_sf_falho[i] != result_sf[i]:
                    print("somou o result falho", inicio, i, soma_total, result_sf_falho[i])
                    soma_total = soma_total + result_sf_falho[i]
                else:
                    print("somou o result normal", inicio, i, soma_total, result_sf[i])
                    soma_total = soma_total + result_sf[i]

        avg = soma_total / (tempo - today)
        avg_no_fail = soma_no_fail / (tempo - today)
        print("peso", peso, (tempo - today))
        print("avg", avg, avg_no_fail)
        average.append(avg)

        list_max.append(max(result_sf))

        if max(result_sf_falho):
            list_fail_max.append(max(result_sf_falho))
        else:
            list_fail_max.append(0)

        desc =  sf.name
        cont = 0

        result_teste_sf = []

        phases = schema.phases.all().order_by('start_date')

        for phase in phases:
            if phase.has_test:
                for i in range(0, int(phase.duration)):
                    result_teste_sf.append(result_sf[cont])
                    result_sf_to_chart.append(0)
                    cont = cont + 1
                if result_sf[cont]:
                    result_teste_sf.append(result_sf[cont])
            else:
                for i in range(0, int(phase.duration)):
                    result_teste_sf.append(0)
                    result_sf_to_chart.append(result_sf[cont])
                    cont = cont + 1

        for i in range(0, tempo):
            if i == today:
                today_result.append(result_sf[i])
                today_result.append(avg)
                td = result_sf[i]
            else:
                today_result.append(0)

            if i > today:
                average_to_chart.append(avg)
            else:
                average_to_chart.append('Null')

        data_to_charts.append({
            'average_to_chart': average_to_chart,
            'result_teste_sf': result_teste_sf,
            'result': result_sf_to_chart,
            'result_sf_falho': result_sf_falho,
            'desc': desc,
            'today_result': today_result
        })

        data_to_table.append({
            'safety_function': sf,
            'today': td,
            'average_fail': avg_no_fail,
            'average': avg,
            'max': max(result_sf)
        })

    start_date = campaign.start_date.replace(tzinfo=None)

    context = {
        'campaign': campaign,
        'start_date':start_date,
        'schema': schema,
        'average': average,
        'maxi': list_max,
        'maxi_fail': list_fail_max,
        'data_to_charts': data_to_charts,
        'data_to_table':data_to_table,
        'today': td,
    }

    return render(request, 'campaigns/campaign_charts.html', context)


def base_case_schema_manager(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    context = {
        'campaign': campaign, 
        'base_schema': campaign.get_schema_active
    }
    return render(request, 'campaigns/base_case_schema_manger.html', context)

# SCHEMAS
def schema_create(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    context = {'campaign': campaign}
    return render(request, 'schemas/schema_form.html', context)


def schema_update(request, schema_pk):
    schema = Schema.objects.prefetch_related('phases').get(pk=schema_pk)
    campaign = schema.campaign
    context = {'schema': schema, 'campaign': campaign}
    return render(request, 'schemas/schema_form.html', context)


def schema_delete(request, schema_pk):
    schema = get_object_or_404(Schema, pk=schema_pk)
    campaign_pk = schema.campaign.pk
    schema.delete()
    messages.success(request, f'Schema "{schema.name}" deleted successfully')
    return redirect('campaigns:index', campaign_pk)


def schema_compare(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    schemas = campaign.schemas.order_by('-name')

    if not campaign.get_schema_active():
        messages.error(
            request, 'You need create a base schema before comparing results')
        return redirect('campaigns:index', campaign.pk)

    relative_comp = []
    relative_comp_max = []
    fl = 0
    final = []
    final_max = []
    for s in schemas:

        #result = ast.literal_eval(s.last_result.values)
        #result_falho = ast.literal_eval(s.last_result.failures)
        result, result_falho = metrics.run(s)

        t = []
        t_max = []
        t.append({'id': s.id, 'name': s.name})
        t_max.append({'id': s.id, 'name': s.name})
        average_schema = []
        max_schema = []

        # result = ast.literal_eval(s.last_result.values)
        tempo = len(result) - 1
        number_sf = len(result[0])

        for j in range(1, number_sf):
            intermediario = []
            intermediario_max = []
            m = []
            soma = 0

            # começando no tempo = 2 conforme excel,
            # eliminar os 2 primeiros elementos do resultado
            for i in range(2, tempo):
                soma = soma + float(result[i][j])
                m.append(float(result[i][j]))

            avg = soma / tempo

            maximo = max(m)

            if fl == 0:
                compare = 1
                compare_max = 1
                relative_comp.append(avg)
                relative_comp_max.append(maximo)
            else:
                compare = avg / relative_comp[j - 1]
                compare_max = maximo / relative_comp_max[j - 1]

            intermediario.append(avg)
            intermediario.append(compare)
            intermediario_max.append(maximo)
            intermediario_max.append(compare_max)

            average_schema.append(intermediario)
            max_schema.append(intermediario_max)
        fl = 1
        t.append(average_schema)
        t_max.append(max_schema)
        final.append(t)
        final_max.append(t_max)

    messages.success(request, 'All schemas had theirs results updated!')
    print(final, final_max)
    context = {
        'safety_functions': campaign.bop.safety_functions.all(),
        'campaign': campaign,
        'averages': final,
        'maxi': final_max,
        'bop': campaign.bop,
        'number_sf': number_sf
    }
    print(datetime.datetime.today(), "Fim ")
    return render(request, 'schemas/schema_compare.html', context)


@transaction.atomic
def schema_clone(request, schema_pk):
    schema = get_object_or_404(Schema, pk=schema_pk)

    clone = Schema.objects.create(name=f'{schema.name} clone',
                                  is_default=False,
                                  schema=schema,
                                  campaign=schema.campaign)

    for p in schema.phases.all():
        phase = Phase.objects.create(name=p.name,
                                     schema=clone,
                                     duration=p.duration,
                                     has_test=p.has_test,
                                     start_date=p.start_date,
                                     is_drilling=p.is_drilling)

        phase.test_groups.set(p.test_groups.values_list('id', flat=True).all())

    compare_schemas_for_campaign.delay(campaign_id=clone.campaign.id,
                                       user_id=request.user.pk)

    messages.success(request, f'Schema "{schema.name}" cloned successfully')
    return redirect('campaigns:schema_active_dashboard', schema.campaign.pk)


# EVENTS
def event_create(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    bop = campaign.bop
    failure_modes = bop.failure_modes
    components = bop.components
    subsystems = bop.subsystems.order_by('code')
    form = EventForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.created_by = request.user
            new_event.campaign_id = campaign_pk
            new_event.save()

            # creates a new results for schema base
            # due the changes made on campaign
            create_new_result_for_schema_base.delay(user_id=request.user.id,
                                                    campaign_id=campaign.id)

            messages.success(request, 'Event created successfully!')
            return redirect(new_event.success_url())

    context = {
        'form': form,
        'campaign': campaign,
        'failure_modes': failure_modes,
        'components': components,
        'subsystems': subsystems
    }

    return render(request, 'events/event_form.html', context)


def event_update(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    form = EventForm(request.POST or None, instance=event)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            # creates a new results for schema base
            # due the changes made on campaign
            create_new_result_for_schema_base.delay(user_id=request.user.id,
                                                    campaign_id=campaign.id)

            messages.success(
                request, f'Event "{event.name}" updated successfully!')
            return redirect(event.success_url())

    context = {'form': event, 'form': form, 'campaign_pk': event.campaign.pk}
    return render(request, 'events/event_form.html', context)


def event_list(request):
    return render(request, 'events/event_list.html')


def event_delete(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    campaign_pk = event.campaign.pk

    if request.method == 'POST':
        event.delete()
        messages.success(
            request, f'Event deleted successfully')
        return redirect('campaigns:index', campaign_pk)


def compare_sf(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    schemas = campaign.schemas.order_by('-name')
    sf_number = int(request.GET.get('sf_number'))
    print("sf o q veio", sf_number)

    data_to_charts = []
    data_to_table = []
    average = []
    maxi = []
    for s in schemas:
        results, result_falho = run(s)
        result_sf = []
        tempo = len(results) - 1
        result_sf_to_chart = []
        average_to_chart = []

        today_result = []

        soma_total = 0
        soma_no_fail = 0
        peso = 0
        td = 0

        for i in range(0, tempo):
            result_sf.append(results[i][sf_number])
            soma_no_fail = soma_no_fail + result_sf[i]

        avg = soma_no_fail / (tempo)


        desc = "Schema: " + s.name +" - Safety Function: " + str(sf_number)
        cont = 0

        result_teste_sf = []

        phases = s.phases.all().order_by('start_date')

        for phase in phases:
            if phase.has_test:
                for i in range(0, int(phase.duration)):
                    result_teste_sf.append(result_sf[cont])
                    result_sf_to_chart.append(0)
                    cont = cont + 1
                if result_sf[cont]:
                    result_teste_sf.append(result_sf[cont])
            else:
                for i in range(0, int(phase.duration)):
                    result_teste_sf.append(0)
                    result_sf_to_chart.append(result_sf[cont])
                    cont = cont + 1

        for i in range(0, tempo):
                average_to_chart.append(avg)

        data_to_charts.append({
            'average_to_chart': average_to_chart,
            'result_teste_sf': result_teste_sf,
            'result': result_sf_to_chart,
            'desc': desc,
        })

        data_to_table.append({
            'average': avg,
            'max': max(result_sf)
        })

    start_date = campaign.start_date.replace(tzinfo=None)

    context = {
        'campaign': campaign,
        'start_date':start_date,
        'data_to_charts': data_to_charts,
        'data_to_table': data_to_table,
    }

    return render(request, 'schemas/compare_charts.html', context)


def cut_list(request, schema_pk, sf_pk):
    schema = Schema.objects.get(pk=schema_pk)
    safety = SafetyFunction.objects.prefetch_related('cuts').get(id=sf_pk)
    cuts = safety.cuts.all()
    max_cuts = Cut.objects.filter(safety_function=safety).count()

    corte = 0
    matriz_index = [[' ' for i in range(5)] for j in range(max_cuts)]

    v_integrate = ast.literal_eval(schema.cuts_contribution)

    for cut in cuts:
        fails = cut.failure_modes.split(",")
        falha = 0
        for fail in fails:
            if fail:
                fail_line = Fail_line(fail, v_integrate)
                matriz_index[corte][falha] = fail_line
            else:
                matriz_index[corte][falha] = ' '
            falha = falha + 1
        corte = corte + 1

    result = metrics.calc_cuts_contribuition_this_timestep(
        5, v_integrate, matriz_index)
    mi = []
    for i in range(0, len(result)):
        for j in range(0, 4):
            if result[i][j] == ' ':
                result[i][j] = ' '
            else:
                result[i][j] = v_integrate[result[i][j]][0]

    mi = sorted(
        matriz_index, key=lambda matriz_index: matriz_index[4], reverse=True)

    context = {
        'result': mi,
        'schema': schema,
    }

    return render(request, 'schemas/cut_list.html', context)
