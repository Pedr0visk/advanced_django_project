from django.forms import ModelForm
from .models import Component
from ..bops.models import Bop


class ComponentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        bop_pk = kwargs.pop('bop')
        super(ComponentForm, self).__init__(*args, **kwargs)
        if bop_pk != '':
            bop = Bop.objects.get(pk=bop_pk)
            self.fields['subsystem'].queryset = bop.subsystems.all()
        print(len(self.fields['subsystem'].queryset))

    class Meta:
        model = Component
        fields = ['code', 'name', 'subsystem']
