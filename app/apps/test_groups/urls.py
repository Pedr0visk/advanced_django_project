from django.urls import path, include
from . import views

app_name = 'test_groups'
urlpatterns = [
    path('', views.test_group_list, name='list'),
    path('add/<int:bop_pk>/', views.test_group_create, name='create'),
    path('<int:tg_pk>/change/', views.test_group_update, name='update'),
    path('<int:tg_pk>/delete/', views.test_group_delete, name='delete'),
    path('<int:history_pk>/undo/', views.test_group_undo, name='undo'),
]
