from django.urls import path, include
from . import views

app_name = 'campaigns'
urlpatterns = [
    path('', views.campaign_list, name="list"),
    path('add/<int:bop_pk>/', views.campaign_create, name="create"),
    path('<int:campaign_pk>/', views.campaign_index, name="index"),
    path('<int:campaign_pk>/change/', views.campaign_update, name="update"),
]
