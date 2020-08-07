from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.dashboard, name="manager"),
  path('login/', views.login_page, name="login_manager"),
  path('logout/', views.logout_user, name="logout_manager"),
  path('register/', views.register_page, name="register"),
  path('accounts/', views.accounts_list, name="list_accounts"),
  path('unauthorized/', views.unauthorized_page, name="unauthorized"),
]
