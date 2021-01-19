"""
ASGI config for bop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from apps.campaigns.consumer import CampaignConsumer
from apps.notifications.consumer import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bop.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/notifications/<int:user_id>/',
                 NotificationConsumer.as_asgi()),
            path('ws/campaigns/<int:user_id>/',
                 CampaignConsumer.as_asgi()),
        ]),
    ),
})