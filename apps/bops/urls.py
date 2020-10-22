from django.urls import path
from . import views

app_name = 'bops'
urlpatterns = [
    path('', views.bop_list, name='list'),
    path('upload/', views.bop_upload, name='upload'),
    path('<int:pk>/', views.index, name='index'),
    path('<int:pk>/change/', views.bop_update, name='update'),
    path('<int:pk>/delete/', views.bop_delete, name='delete'),
    path('<int:pk>/test-planner/', views.test_planner, name='test_planner'),
    path('<int:pk>/test-planner/raw/', views.test_planner_raw, name='test_planner_raw'),
    path('<int:pk>/summary-results/', views.summary_results, name='summary_results'),
    path('<int:pk>/subsystems/', views.list_subsystems, name='list_subsystems'),

    path('<int:bop_pk>/safety-functions/',
         views.safety_function_list,
         name='list_safety_functions'),
    path('<int:bop_pk>/safety-functions/upload/',
         views.safety_function_upload,
         name='upload_safety_function'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/',
         views.safety_function_index,
         name='index_safety_function'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/change/',
         views.safety_function_update,
         name='update_safety_function'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/cuts/',
         views.safety_function_cuts,
         name='list_safety_function_cuts'),
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/delete/',
         views.safety_function_delete,
         name='delete_safety_function'),
]
