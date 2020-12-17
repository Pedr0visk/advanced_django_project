from django.apps import AppConfig


class CampaignsConfig(AppConfig):
    """
    we have this "apps."" in front of campaign cause we put all our apps inside
    a folder called "apps"
    """
    name = 'apps.campaigns'

    def ready(self):
        import apps.campaigns.receivers
