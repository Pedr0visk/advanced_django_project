from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.models import User 

from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages

from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users

def registerPage(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      user = form.cleaned_data.get('username')
      messages.success(request, 'Account created Successfully for: ' + user)
      
      return redirect('register')

  context = {'form': form}
  return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

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


def logoutUser(request):
  logout(request)
  return redirect('login')


def dashboard(request):
  return render(request, 'accounts/dashboard.html')


@allowed_users(allowed_roles=['Admin'])
def usersList(request):
  users = User.objects.all()
  context = {'users': users}
  return render(request, 'accounts/users-list.html', context)