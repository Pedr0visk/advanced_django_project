from django.forms import ModelForm
from .models import Bop, SafetyFunction


class BopForm(ModelForm):
    class Meta:
        model = Bop
        fields = ['name', 'rig']


class SafetyFunctionForm(ModelForm):
    class Meta:
        model = SafetyFunction
        fields = ['name' , 'description']