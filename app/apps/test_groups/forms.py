from django.forms import ModelForm, DateInput, Textarea
from .models import TestGroup, TestGroupDummy
from ..failuremodes.models import FailureMode


class TestGroupForm(ModelForm):


    class Meta:
        model = TestGroup
        fields = ['name', 'start_date', 'tests', 'failure_modes']
        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'})
        }


class TestGroupDummyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.bop_pk = kwargs.pop('bop_pk')
        super(TestGroupDummyForm, self).__init__(*args, **kwargs)
        self.fields['failure_modes'].widget.attrs.update({'class': 'selectfilter'})
        self.fields['failure_modes'].queryset = FailureMode.objects.filter(
            component__subsystem__bop=self.bop_pk)

    class Meta:
        model = TestGroupDummy
        fields = ['name', 'start_date', 'tests', 'failure_modes']

        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
            'tests': Textarea(attrs={'class': 'd-none'})
        }
