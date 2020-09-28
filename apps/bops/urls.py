from django.urls import path, include
from . import views
from django.contrib.auth.models import Group, User

urlpatterns = [
    path('', views.bop_list, name='list_bops'),
    path('upload/', views.bop_upload, name='upload_bop'),
    path('<int:pk>/', views.index, name='index_bop'),
    path('<int:pk>/change/', views.bop_update, name='update_bop'),
    path('<int:pk>/delete/', views.bop_delete, name='delete_bop'),
    path('<int:pk>/test-planner/', views.test_planner, name='test_planner'),
    path('<int:pk>/test-planner/raw/', views.test_planner_raw, name='test_planner_raw'),
    path('<int:pk>/test-planner/raw/migrate/', views.migrate, name='test_planner_migrate'),
    path('<int:bop_pk>/campaigns/', include('apps.campaigns.urls')),
    path('<int:bop_pk>/subsystems/', include('apps.subsystems.urls')),
    path('<int:bop_pk>/events/', include('apps.events.urls')),
    path('<int:bop_pk>/components/', include('apps.components.urls')),
    path('<int:bop_pk>/failuremodes/', include('apps.failuremodes.urls')),
    path('<int:bop_pk>/test-groups/', include('apps.test_groups.urls')),
    path('<int:bop_pk>/certifications/', include('apps.certifications.urls')),

    path('<int:bop_pk>/safety-functions/',
         views.safety_function_list,
         name='list_safety_functions'),
    path('<int:bop_pk>/safety-functions/upload/',
         views.safety_function_upload,
         name='upload_safety_function'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/',
         views.safety_function_index,
         name='index_safety_function'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/cuts/',
         views.safety_function_cuts,
         name='list_safety_function_cuts'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/delete/',
         views.safety_function_delete,
         name='delete_safety_function'),
]
