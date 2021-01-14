from channels.generic.websocket import AsyncJsonWebsocketConsumer


class CampaignConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        print("CONNECTED CAMPAIGN", event)

        await self.channel_layer.group_add(
            f"campaign_group_{self.scope['url_route']['kwargs']['user_id']}",
            self.channel_name
        )

        await self.accept()

    async def websocket_disconnect(self, event):
        print("DISCONNECTED", event)

    async def websocket_receive(self, event):
        print("RECEIVE CAMPAIGN", event)
        await self.send(text_data='HELLO')

    async def campaign_info(self, event):
        print('[LOGGER]', 'campaign_info', event)
        await self.send_json({
            'type': event['group'],
            'message': event['body']
        })
