from rest_framework import serializers

from apps.campaigns.models import Campaign, Phase, Schema
from apps.test_groups.models import TestGroup
from ..tasks import *

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

        # toggle default in schemas table
        if schema.is_default:
            Schema.toggle_schema_default(schema)

        if not schema.campaign.get_schema_active():
            schema.is_default = True
            schema.save()

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            phase = Phase.objects.create(schema=schema, **phase_data)
            if phase.has_test:
                phase.test_groups.set(test_groups)

        compare_schemas_for_campaign.delay(campaign_id=schema.campaign.id,
                                           user_id=user.pk)

        return schema

    def update(self, instance, validated_data):
        phases_data = validated_data.pop('phases')
        instance.name = validated_data.get('name', instance.name)
        instance.is_default = validated_data.get('is_default', instance.name)
        instance.save()
        instance.phases.all().delete()

        # getting user from request
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        for phase_data in phases_data:
            test_groups = phase_data.pop('test_groups')
            phase = Phase.objects.create(schema=instance, **phase_data)
            if phase.has_test:
                phase.test_groups.set(test_groups)

        if not instance.campaign.active:
            compare_schemas_for_campaign.delay(campaign_id=instance.campaign.id,
                                               user_id=user.pk)

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
