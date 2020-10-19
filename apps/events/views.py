from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event

# dependencies
from apps.campaigns.models import Campaign
from apps.failuremodes.models import FailureMode
from apps.components.models import Component
from apps.subsystems.models import Subsystem


def event_create(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    bop = campaign.bop

    form = EventForm(request.POST or None)
    failure_modes = FailureMode.objects.filter(component__subsystem__bop=bop)
    components = Component.objects.filter(subsystem__bop=bop)
    subsystems = Subsystem.objects.filter(bop=bop)

    if request.method == 'POST':
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.campaign_id = campaign_pk
            new_event.save()
            messages.success(request, f'Event "{new_event.name}" created successfully!')
            return redirect(new_event.success_url())

    context = {
        'form': form,
        'campaign_pk': campaign_pk,
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
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect(event.success_url())

    context = {'form': event, 'form': form, 'campaign_pk': event.campaign.pk}
    return render(request, 'events/event_form.html', context)


def event_list(request):
    return render(request, 'events/event_list.html')


"""
    {name: 'event 1', type: 'fmode_fail', _id: 'abc123'}
    if type == 'fmode_fail':
        FailureMode.objects.get(pk=_id)
    if type == 'comp_fail':
        Component.objects.get(pk=_id)
    if type == 'subsys_fail':
        Subsystem.objects.get(pk=_id)

"""
