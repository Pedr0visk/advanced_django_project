from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User


class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
