from rest_framework import serializers
from apps.test_groups.models import TestGroup
from apps.failuremodes.api.serializers import FailureModeSerializer


class TestGroupSerializer(serializers.ModelSerializer):
    failure_modes = FailureModeSerializer(read_only=True, many=True)

    class Meta:
        model = TestGroup
        fields = (
            'id', 'name', 'tests', 'failure_modes'
        )
