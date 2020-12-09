from django.urls import path, include
from . import views

app_name = 'failuremodes'

urlpatterns = [
    path('', views.failuremode_list, name='list'),
    path('add/', views.failuremode_create, name='create'),
    path('<int:fm_pk>/change/', views.failuremode_update, name='update'),
]
