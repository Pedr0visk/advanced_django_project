from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django.core import serializers


class CampaignConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        print("CONNECTED CAMPAIGN", event)

        await self.channel_layer.group_add(
            f"notification_group_{self.scope['url_route']['kwargs']['campaign_id']}",
            self.channel_name
        )

        await self.accept()

    async def websocket_disconnect(self, event):
        print("DISCONNECTED", event)

    async def websocket_receive(self, event):
        print("RECEIVE", event)
        await self.send(text_data='HELLO')

    async def campaign_info(self, event):
        print('[LOGGER]', 'campaign_info', event)
