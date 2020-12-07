from django.urls import path, include
from . import views

app_name = 'subsystems'

urlpatterns = [
    path('', views.subsystem_list, name='list'),
    path('<int:s_pk>/', views.index, name='index_subsystem'),
]
