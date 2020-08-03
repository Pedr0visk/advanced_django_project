from django.urls import path
from . import views

urlpatterns = [
  path('', views.dashboard, name="dashboard"),
  path('login/', views.loginPage, name="login"),
  path('register/', views.registerPage, name="register"),
  path('logout/', views.logoutUser, name="logout"),
  path('users-list/', views.usersList, name="list_users"),
]
