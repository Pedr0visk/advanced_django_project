from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='list_events'),
    path('add/<int:campaign_pk>/', views.event_create, name='create'),
]
