from django.apps import AppConfig


class BopsConfig(AppConfig):
    name = 'apps.bops'

    def ready(self):
        import apps.bops.signals
        import apps.bops.receivers
