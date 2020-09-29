from rest_framework import serializers
from apps.campaigns.models import Campaign, Phase


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('name',
                  'start_date',
                  'end_date',
                  'bop',
                  'active',
                  'well_name',
                  'description')


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ('name',
                  'start_date',
                  'campaign',
                  'step',
                  'duration')
