"""
ASGI config for bop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
import os

from django.conf.urls import url
from django.core.asgi import get_asgi_application
# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bop.settings')
django_asgi_app = get_asgi_application()
print(django_asgi_app)

from apps.notifications.consumer import NotificationConsumer
from apps.campaigns.consumer import CampaignConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack




application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/notifications/$", NotificationConsumer.as_asgi()),
            url(r"^ws/campaigns/$", CampaignConsumer.as_asgi()),
        ]),
    ),
})
