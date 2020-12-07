from django.urls import path, include
from . import views

app_name = 'subsystems'

urlpatterns = [
    path('', views.subsystem_list, name='list'),
    path('add/', views.subsystem_create, name='create'),
    path('/<int:subsystem_pk>/change/', views.subsystem_update, name='update'),
    path('/<int:subsystem_pk>/delete/', views.subsystem_delete, name='delete'),
    path('<int:s_pk>/', views.index, name='index_subsystem'),
]
