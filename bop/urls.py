from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.campaigns.api.views import CampaignViewSet
from apps.bops.api.views import BopViewSet

router = routers.DefaultRouter()
router.register('campaigns', CampaignViewSet)
router.register('bops', BopViewSet)

urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('bops/', include('apps.bops.urls')),
    path('cuts/', include('apps.cuts.urls')),
    path('admin/', admin.site.urls),
    path('manager/', include('apps.managers.urls')),
    path('campaigns/', include('apps.campaigns.urls')),
    path('events/', include('apps.events.urls')),
    path('test-groups/', include('apps.test_groups.urls')),
    # api
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
