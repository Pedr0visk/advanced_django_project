from django.urls import path
from . import views

urlpatterns = [
  path('', views.dashboard, name="operator_dashboard"),
  path('login/', views.login_page, name="login"),
  path('logout/', views.logout_user, name="logout"),
  path('register/', views.register_page, name="register"),
  path('users-list/', views.users_list, name="list_users"),
]
