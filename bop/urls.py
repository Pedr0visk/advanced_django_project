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
    path('api-auth/', include('rest_framework.urls')),
    # api
    path('api/', include(router.urls))
]
