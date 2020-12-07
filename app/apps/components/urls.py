from django.urls import path, include
from . import views

app_name = 'components'

urlpatterns = [
    path('', views.component_list, name='list'),
    path('<int:c_pk>/', views.index, name='index'),
]
