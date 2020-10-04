from rest_framework import serializers
from apps.test_groups.models import TestGroup, TestSchedule


class TestGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestGroup
        fields = (
            'id', 'name'
        )


class TestScheduleSerializer(serializers.ModelSerializer):
    test_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = TestSchedule
        fields = ('date', 'test_groups', 'phase')
