from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.certification_list, name='list_certifications'),
    path('<int:cert_pk>/change/', views.certification_update, name='update_certification'),
]
