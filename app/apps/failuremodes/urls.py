from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.failuremode_list, name='list_failuremodes'),
    path('<int:fm_pk>/change/', views.failuremode_update, name='update_failuremode'),
]
