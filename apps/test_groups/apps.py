from django.apps import AppConfig


class TestGroupsConfig(AppConfig):
    name = 'apps.test_groups'

    def ready(self):
        import apps.test_groups.signals
