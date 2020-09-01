from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.failuremode_list, name='list_failuremodes'),
    path('<slug:slug>/', views.index, name='index_failuremode'),
]
