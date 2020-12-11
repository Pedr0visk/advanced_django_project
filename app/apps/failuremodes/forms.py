from django.forms import ModelForm
from django.contrib.postgres.fields import JSONField
from .models import FailureMode


class FailureModeForm(ModelForm):
    class Meta:
        model = FailureMode
        fields = ['code', 'name', 'distribution', 'diagnostic_coverage', 'component']
