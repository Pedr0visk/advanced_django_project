from django.forms import ModelForm, DateInput, MultipleChoiceField
from .models import TestGroup, TestGroupDummy
from ..failuremodes.models import FailureMode


class TestGroupForm(ModelForm):
    class Meta:
        model = TestGroup
        fields = ['start_date', 'tests', 'failure_modes']

        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }


class TestGroupDummyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.bop = kwargs.pop('bop')
        super(TestGroupDummyForm, self).__init__(*args, **kwargs)
        self.fields['failure_modes'].widget.attrs.update({'class': 'selectfilter'})
        self.fields['failure_modes'].queryset = FailureMode.objects.filter(
            component__subsystem__bop__exact=self.bop)

    class Meta:
        model = TestGroupDummy
        fields = ['start_date', 'tests', 'failure_modes']

        widgets = {
            'start_date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
