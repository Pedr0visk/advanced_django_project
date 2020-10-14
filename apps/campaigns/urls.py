from django.urls import path, include
from . import views

app_name = 'campaigns'
urlpatterns = [
    path('', views.campaign_list, name="list"),
    path('add/<int:bop_pk>/', views.campaign_create, name="create"),
    path('<int:campaign_pk>/', views.campaign_index, name="index"),
    path('<int:campaign_pk>/change/', views.campaign_update, name="update"),
    path('schemas/<int:pk>/change/', views.phase_update, name="update_phase"),
    path('<int:campaign_pk>/run/', views.campaign_metrics, name="run"),
    path('<int:campaign_pk>/schemas/add/', views.schema_create, name="create_schema"),
    path('<int:campaign_pk>/schemas/<int:schema_pk>/', views.schema_index, name="schema_index"),
    path('<int:campaign_pk>/schemas/<int:schema_pk>/delete/',
         views.schema_delete,
         name="delete_schema"),
    path('<int:campaign_pk>/schemas/<int:schema_pk>/change/',
         views.schema_update,
         name="change_schema"),
]
