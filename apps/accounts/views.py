from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .decorators import unauthenticated_user
from .forms import UpdateProfileForm


@login_required(login_url='/login/')
def profile_update(request):
    user = request.user
    form = UpdateProfileForm(instance=user)
    context = {'form': form}

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('update_profile')

    return render(request, 'accounts/profile_form.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "username or email is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
