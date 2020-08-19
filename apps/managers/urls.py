from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name="manager"),
    # auth
    path('login/', views.login_page, name="login_manager"),
    path('logout/', views.logout_user, name="logout_manager"),
    path('unauthorized/', views.unauthorized_page, name="unauthorized"),
    # accounts
    path('accounts/', views.account_list, name="list_accounts"),
    path('accounts/add/', views.account_register, name="register_account"),
    path('accounts/<int:pk>/change/', views.account_update, name="update_account"),
    path('accounts/<int:pk>/delete/', views.account_delete, name="delete_account"),
    path('accounts/<int:pk>/password/', views.password_change, name="change_password"),

    path('bops/', include('apps.bops.urls')),
]
