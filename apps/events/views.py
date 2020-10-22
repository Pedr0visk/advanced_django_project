from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event

# dependencies
from apps.campaigns.models import Campaign


def event_create(request, campaign_pk):
    campaign = Campaign.objects.get(pk=campaign_pk)
    bop = campaign.bop

    form = EventForm(request.POST or None)
    failure_modes = bop.failure_mode_list()
    components = bop.component_list()
    subsystems = bop.subsystems.all()

    if request.method == 'POST':
        if form.is_valid():
            print(request.POST)
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
