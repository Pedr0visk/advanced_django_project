from django.urls import path, include
from . import views

app_name = 'components'

urlpatterns = [
    path('', views.component_list, name='list'),
    path('add/', views.component_create, name='create'),
    path('<int:component_pk>/change/', views.component_update, name='update'),
    path('<int:component_pk>/delete/', views.component_delete, name='delete'),
    path('<int:c_pk>/', views.index, name='index'),
]
