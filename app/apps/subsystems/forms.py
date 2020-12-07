from django.forms import ModelForm

from apps.subsystems.models import Subsystem


class SubsystemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        bop = kwargs.pop('bop')
        super(SubsystemForm, self).__init__(*args, **kwargs)
        self.fields['bop'].initial = bop

    class Meta:
        model = Subsystem
        fields = ['bop', 'code', 'name']
