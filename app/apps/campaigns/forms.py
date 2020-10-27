from django.forms import ModelForm, DateInput, DateTimeInput, IntegerField
from .models import Campaign, Phase


class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ['name',
                  'description',
                  'active',
                  'well_name',
                  'start_date',
                  'end_date']
        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': DateInput(format='%Y-%m-%d',
                                  attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }


class PhaseForm(ModelForm):
    class Meta:
        model = Phase
        fields = ['name', 'duration', 'start_date']
        widgets = {
            'start_date': DateTimeInput(format='%Y-%m-%d',
                                        attrs={'placeholder': 'Select a date', 'type': 'date'}),

        }

