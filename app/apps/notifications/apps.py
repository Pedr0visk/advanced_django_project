from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'

    def ready(self):
        import apps.notifications.receivers
