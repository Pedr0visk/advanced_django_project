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
                  'status',
                  'start_date',
                  'end_date']
        widgets = {
            'start_date': DateInput(format=('%m/%d/%Y'),
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': DateInput(format=('%m/%d/%Y'),
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
