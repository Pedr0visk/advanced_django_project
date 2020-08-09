from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.dashboard, name="manager"),
  # auth
  path('login/', views.login_page, name="login_manager"),
  path('logout/', views.logout_user, name="logout_manager"),
  path('unauthorized/', views.unauthorized_page, name="unauthorized"),
  # accounts
  path('register_account/', views.account_register, name="register_account"),
  path('update_account/', views.account_update, name="update_account"),
  path('list_accounts/', views.account_list, name="list_accounts"),
  
]
