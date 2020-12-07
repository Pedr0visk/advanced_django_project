from django.forms import ModelForm

from apps.subsystems.models import Subsystem


class SubsystemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        query_params = kwargs.pop('query_params')
        super(SubsystemForm, self).__init__(*args, **kwargs)
        self.fields['bop'].initial = query_params['bop']

    class Meta:
        model = Subsystem
        fields = ['bop', 'code', 'name']
