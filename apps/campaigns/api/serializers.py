from django.contrib import messages
from rest_framework import serializers
from apps.campaigns.models import Campaign, Phase
from apps.test_groups.models import TestSchedule


class PhaseSerializer(serializers.ModelSerializer):
    step = serializers.ChoiceField(choices=Phase.Step.choices)
    test_groups = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Phase
        fields = (
            'name', 'step', 'test_groups',
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
        print(phases_data)
        campaign = Campaign.objects.create(**validated_data)

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            if phase_data['step'] == Phase.Step.TEST:
                new_phase = Phase.objects.create(campaign=campaign, **phase_data)
                scheduler = TestSchedule.objects.create(phase=new_phase,
                                                        date=new_phase.start_date)
                scheduler.test_groups.set(test_groups)
            else:
                Phase.objects.create(campaign=campaign, **phase_data)

        return campaign
