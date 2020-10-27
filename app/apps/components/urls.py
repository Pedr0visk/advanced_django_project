from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.component_list, name='list_components'),
    path('<int:c_pk>/', views.index, name='index_component'),
]
