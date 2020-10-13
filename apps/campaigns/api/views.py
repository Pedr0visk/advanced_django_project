from rest_framework import viewsets
from .serializers import CampaignSerializer
from apps.campaigns.models import Campaign


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

