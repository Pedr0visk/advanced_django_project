from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.certification_list, name='list_certifications'),
]
