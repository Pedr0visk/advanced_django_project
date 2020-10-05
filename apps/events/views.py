from django.shortcuts import render, redirect
from .forms import EventForm


def event_create(request, campaign_pk):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.campaign_id = campaign_pk
            new_event.save()
            return redirect(new_event.success_url())

    context = {'form': form, 'campaign_pk': campaign_pk}
    return render(request, 'events/event_form.html', context)


def event_list(request):
    return render(request, 'events/event_list.html')
