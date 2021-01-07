from django.urls import path

from . import consumer

websocket_urlpatterns = [
    path('ws/campaigns/<int:campaign_id>/',
         consumer.CampaignConsumer.as_asgi()),
]
