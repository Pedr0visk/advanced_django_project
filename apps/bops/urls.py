from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.upload, name="upload_bop"),
    path('<int:pk>/campaigns/', views.campaigns_list, name="list_bop__campaigns")
]
