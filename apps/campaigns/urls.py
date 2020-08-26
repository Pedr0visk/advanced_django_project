from django.urls import path, include
from . import views

"""
Each url of campaigns apps expect a bop_pk because we are 
handling a associate campaign that belongs to this bop. 
Ex of url: /bop/1/campaigns/2/change/
"""
urlpatterns = [
    path('', views.campaign_list, name="list_campaigns"),
    path('add/', views.campaign_create, name="create_campaign"),
    path('<int:campaign_pk>/change/', views.campaign_update, name="update_campaign")
]
