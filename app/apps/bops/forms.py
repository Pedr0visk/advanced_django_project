from django.forms import ModelForm, forms, DateInput
from .models import Bop, SafetyFunction, Certification


class BopForm(ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Bop
        fields = ['name', 'rig', 'model']


class SafetyFunctionForm(ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = SafetyFunction
        fields = ['name', 'description']


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
