from django.apps import AppConfig


class FailuremodesConfig(AppConfig):
    name = 'apps.failuremodes'

    def ready(self):
        import apps.failuremodes.signals

