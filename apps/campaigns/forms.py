from django.forms import ModelForm, DateInput
from .models import Campaign


class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ['name',
                  'description',
                  'active',
                  'rig_name',
                  'well_name',
                  'start_date',
                  'end_date']
        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': DateInput(format='%Y-%m-%d',
                                  attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
