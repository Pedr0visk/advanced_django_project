from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.upload, name="upload_bop"),
    path('<int:bop_pk>/campaigns/', include('apps.campaigns.urls'))
]
