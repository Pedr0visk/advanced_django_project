from django.forms import ModelForm, DateInput
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'type', 'object_code', 'description', 'date']
        widgets = {
            'date': DateInput(format='%Y-%m-%d',
                                    attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }
