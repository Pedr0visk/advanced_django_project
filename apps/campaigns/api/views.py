from rest_framework import viewsets
from .serializers import CampaignSerializer, SchemaSerializer
from apps.campaigns.models import Campaign, Schema


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer


