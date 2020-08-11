from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
