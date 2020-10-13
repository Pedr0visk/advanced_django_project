from rest_framework import serializers
from apps.campaigns.models import Campaign, Phase, Schema


class PhaseSerializer(serializers.ModelSerializer):
    test_groups = serializers.ListField(child=serializers.IntegerField(), required=False)

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
        fields = ('name', 'schemas',)


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
