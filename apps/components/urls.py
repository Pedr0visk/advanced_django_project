from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.component_list, name='list_components'),
]
