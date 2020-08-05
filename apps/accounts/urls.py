from django.urls import path
from . import views

urlpatterns = [
  path('', views.dashboard, name="dashboard"),
  path('login/', views.login_page, name="login"),
  path('register/', views.register_page, name="register"),
  path('logout/', views.logout_user, name="logout"),
  path('users-list/', views.users_list, name="list_users"),
]
