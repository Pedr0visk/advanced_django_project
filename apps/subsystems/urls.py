from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.subsystem_list, name='list_subsystems'),
    path('<slug:slug>/', views.index, name='index_subsystem'),
]
