import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.bops.api.views import BopViewSet
from apps.campaigns.api.views import CampaignViewSet, SchemaViewSet

router = routers.DefaultRouter()
router.register('campaigns', CampaignViewSet)
router.register('schemas', SchemaViewSet)
router.register('bops', BopViewSet)

urlpatterns = [
    path('', include('apps.accounts.urls')),
    path('', include('apps.campaigns.urls')),

    path('bops/', include('apps.bops.urls')),
    path('cuts/', include('apps.cuts.urls')),
    path('admin/', admin.site.urls),
    path('manager/', include('apps.managers.urls')),
    path('certifications/', include('apps.certifications.urls')),
    path('test-groups/', include('apps.test_groups.urls')),
    path('subsystems/', include('apps.subsystems.urls')),
    # api
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    #debug
    path('__debug__/', include(debug_toolbar.urls))
]
