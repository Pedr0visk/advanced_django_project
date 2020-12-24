from django.forms import ModelForm, DateInput
from .models import Certification


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ['start_date', 'end_date']

        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'class': 'form-control datetimepicker-input',
                                           'data-target': '#datetimepicker1'}),
            'end_date': DateInput(format='%Y-%m-%d',
                                  attrs={'class': 'form-control datetimepicker-input',
                                         'data-target': '#datetimepicker2'}),
        }
