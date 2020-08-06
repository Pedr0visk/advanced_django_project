from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('', include('apps.accounts.urls')),
  path('manager/', include('apps.managers.urls')),
  path('admin/', admin.site.urls),
]
