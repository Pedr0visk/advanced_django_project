from django.urls import path
from . import views

app_name = 'bops'
urlpatterns = [
    # bop
    path('upload/', views.bop_upload, name='upload'),
    path('<int:pk>/dashboard/', views.index, name='index'),
    path('<int:pk>/hierarchy/', views.bop_hierarchy, name='hierarchy'),
    path('<int:pk>/change/', views.bop_update, name='update'),
    path('<int:pk>/delete/', views.bop_delete, name='delete'),
    path('<int:pk>/results/', views.bop_result, name='results'),

    # test planner
    path('<int:pk>/test-planner/', views.test_planner, name='test_planner'),
    path('<int:pk>/test-planner/raw/',
         views.test_planner_raw, name='test_planner_raw'),

    # safety functions
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
    path('<int:bop_pk>/safety-functions/<int:sf_pk>/delete/',
         views.safety_function_delete,
         name='delete_safety_function'),
]
