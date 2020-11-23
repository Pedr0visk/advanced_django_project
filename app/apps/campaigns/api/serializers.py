from rest_framework import serializers

from apps.campaigns.models import Campaign, Phase, Schema
from apps.test_groups.models import TestGroup


class PhaseSerializer(serializers.ModelSerializer):
    test_groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TestGroup.objects.all())

    class Meta:
        model = Phase
        fields = (
            'name', 'test_groups', 'has_test', 'is_drilling',
            'start_date', 'duration'
        )


class SchemaSerializer(serializers.ModelSerializer):
    phases = PhaseSerializer(many=True)

    class Meta:
        model = Schema
        fields = ('name', 'phases', 'campaign', 'is_default')

    def create(self, validated_data):
        phases_data = validated_data.pop('phases')
        schema = Schema.objects.create(**validated_data)

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            phase = Phase.objects.create(schema=schema, **phase_data)
            if phase.has_test:
                phase.test_groups.set(test_groups)

        return schema

    def update(self, instance, validated_data):
        phases_data = validated_data.pop('phases')
        instance.name = validated_data.get('name', instance.name)
        instance.is_default = validated_data.get('is_default', instance.name)
        instance.save()
        instance.phases.all().delete()

        # toggle default in schemas table
        if instance.is_default:
           Schema.toggle_schema_default(instance.name)

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            phase = Phase.objects.create(schema=instance, **phase_data)
            if phase.has_test:
                phase.test_groups.set(test_groups)

        return instance


class CampaignSerializer(serializers.ModelSerializer):
    schemas = SchemaSerializer()

    class Meta:
        model = Campaign
        fields = (
            'name', 'start_date', 'end_date', 'schemas',
            'bop', 'active', 'well_name', 'description'
        )

    def create(self, validated_data):
        schema_data = validated_data.pop('schemas')
        phases_data = schema_data.pop('schemas')
        campaign = Campaign.objects.create(**validated_data)
        schema = Schema.objects.create(campaign=campaign, **schema_data)

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            phase = Phase.objects.create(schema=schema, **phase_data)
            if phase_data['has_test']:
                phase.test_groups.set(test_groups)

        return campaign
