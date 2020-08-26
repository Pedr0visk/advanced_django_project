from django.forms import ModelForm
from .models import Bop


class BopForm(ModelForm):
    class Meta:
        model = Bop
        fields = ['name', 'rig']
