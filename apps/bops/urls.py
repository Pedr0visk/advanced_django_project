from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bop_list, name='list_bops'),
    path('upload/', views.upload, name='upload_bop'),
    path('<int:pk>/', views.index, name='index_bop'),
    path('<int:pk>/change/', views.bop_update, name='update_bop'),
    path('<int:bop_pk>/campaigns/', include('apps.campaigns.urls')),
    path('<int:bop_pk>/subsystems/', include('apps.subsystems.urls')),
    path('<int:bop_pk>/components/', include('apps.components.urls')),
    path('<int:bop_pk>/failuremodes/', include('apps.failuremodes.urls')),
]
