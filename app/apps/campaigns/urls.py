from django.urls import path
from . import views

app_name = 'campaigns'
urlpatterns = [
    # schemas
    path('campaigns/', views.campaign_list, name="list"),
    path('campaigns/add/<int:bop_pk>/', views.campaign_create, name="create"),
    path('campaigns/<int:campaign_pk>/dashboard/',
         views.campaign_index, name="index"),
    path('campaigns/<int:campaign_pk>/planner/',
         views.campaign_planner, name="planner"),
    path('campaigns/<int:campaign_pk>/change/',
         views.campaign_update, name="update"),
    path('campaigns/<int:campaign_pk>/delete/',
         views.campaign_delete, name="delete"),
    path('campaigns/<int:campaign_pk>/compare/',
         views.schema_compare, name="compare"),
    path('campaigns/<int:campaign_pk>/compare_sf/',
         views.compare_sf, name="compare_sf"),
    path('campaigns/<int:campaign_pk>/run/', views.campaign_run, name="run"),

    # schemas
    path('schemas/<int:campaign_pk>/run/',
         views.campaign_metrics, name="metrics"),
    path('schemas/<int:schema_pk>/change/',
         views.schema_update, name="update_schema"),
    path('schemas/add/<int:campaign_pk>/',
         views.schema_create, name="create_schema"),
    path('schemas/<int:schema_pk>/delete/',
         views.schema_delete, name="delete_schema"),
    path('schemas/<int:schema_pk>/<int:sf_pk>/cut_list/',
         views.cut_list, name="cut_list"),
    path('schemas/clone/<int:schema_pk>/',
         views.schema_clone, name="clone_schema"),

    # events
    path('events/add/<int:campaign_pk>/',
         views.event_create, name="create_event"),
    path('events/delete/<int:event_pk>',
         views.event_delete, name="delete_event"),
]
