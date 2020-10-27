from rest_framework import serializers
from apps.test_groups.models import TestGroup


class TestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestGroup
        fields = (
            'id', 'name'
        )
