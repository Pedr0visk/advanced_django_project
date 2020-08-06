from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .decorators import unauthenticated_user


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
