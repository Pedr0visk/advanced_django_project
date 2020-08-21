from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('', include('apps.accounts.urls')),
  path('bops/', include('apps.bops.urls')),
  path('admin/', admin.site.urls),
  path('manager/', include('apps.managers.urls')),

]
