from rest_framework import serializers
from apps.campaigns.models import Campaign, Phase


class PhaseSerializer(serializers.ModelSerializer):
    test_groups = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Phase
        fields = (
            'name', 'test_groups',
            'start_date', 'duration'
        )


class CampaignSerializer(serializers.ModelSerializer):
    phases = PhaseSerializer(many=True)

    class Meta:
        model = Campaign
        fields = (
            'name', 'start_date', 'end_date',
            'bop', 'active', 'well_name', 'description', 'phases'
        )

    def create(self, validated_data):
        phases_data = validated_data.pop('phases')
        campaign = Campaign.objects.create(**validated_data)

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            if phase_data['has_test']:
                new_phase = Phase.objects.create(campaign=campaign, **phase_data)
            else:
                Phase.objects.create(campaign=campaign, **phase_data)

        return campaign
