from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/change/', views.profile_update, name="update_profile"),
    path('profile/password_change/', views.password_change, name="password_change"),

    path('profile/reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),

    path('profile/reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),

    path('profile/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path('profile/reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete")
]
