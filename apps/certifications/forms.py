from django.forms import ModelForm, DateInput
from .models import Certification


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ['start_date', 'end_date', 'code']

        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': DateInput(format='%Y-%m-%d',
                                  attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
