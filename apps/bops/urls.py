from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.upload, name="upload_bop"),
    path('<int:pk>/campaigns/', views.campaign_list, name="list_bop__campaigns"),
    path('<int:pk>/campaigns/add/', views.campaign_create, name="create_campaign"),
    path('<int:bop_pk>/campaigns/', include('apps.campaigns.urls'))
]
