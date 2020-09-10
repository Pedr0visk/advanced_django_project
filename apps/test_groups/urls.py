from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.test_group_list, name='list_test_groups'),
    path('add/', views.test_group_create, name='create_test_group'),
]
