from django.forms import ModelForm, forms
from .models import Bop, SafetyFunction


class BopForm(ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Bop
        fields = ['name', 'rig']


class SafetyFunctionForm(ModelForm):
    file = forms.FileField()

    class Meta:
        model = SafetyFunction
        fields = ['name', 'description']
