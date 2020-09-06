from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cut_list, name='list_cuts'),

]
