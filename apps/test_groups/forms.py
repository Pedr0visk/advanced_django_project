from django.forms import ModelForm, DateInput
from .models import TestGroup


class TestGroupForm(ModelForm):
    class Meta:
        model = TestGroup
        fields = ['start_date', 'tests', 'failure_modes']

        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
