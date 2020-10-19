from django.urls import path, include
from . import views

app_name = 'cuts'
urlpatterns = [
    path('', views.cut_list, name='list'),

]
