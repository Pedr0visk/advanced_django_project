from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.dashboard, name="dashboard"),
  path('login/', views.login_page, name="login"),
  path('accounts/', views.accounts_list, name="list_accounts"),
]
