from rest_framework import serializers
from apps.failuremodes.models import FailureMode


class FailureModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailureMode
        fields = (
            'id', 'name', 'code'
        )
