from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.dashboard, name="dashboard"),
  path('login/', views.login_page, name="login"),
  path('logout/', views.logout_user, name="logout"),
  path('profile/change/', views.profile_update, name="update_profile")
]
