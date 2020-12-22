from django.forms import ModelForm, DateInput, DateTimeInput, CharField, TextInput
from .models import Campaign, Phase, Event


class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ['name',
                  'description',
                  'well_name']


class PhaseForm(ModelForm):
    class Meta:
        model = Phase
        fields = ['name', 'duration', 'start_date']
        widgets = {
            'start_date': DateTimeInput(format='%Y-%m-%d',
                                        attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }


class EventForm(ModelForm):
    object_code = CharField(widget=TextInput(attrs={'class': 'd-none ',
                                                    'id': 'object_code'}))

    class Meta:
        model = Event
        fields = ['type', 'object_code', 'description', 'date']

        widgets = {
            'date': DateInput(format='%Y-%m-%d',
                              attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
