from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import CreateUserForm
from .models import Employer
from .decorators import unauthenticated_user, allowed_users

def registerPage(request):

  form = CreateUserForm()
  groups = Group.objects.all()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      group = Group.objects.get(pk=request.POST['group'])

      user = form.save()
      user.groups.add(group)
      Employer.objects.create(user=user,)

      username = form.cleaned_data.get('username')
      messages.success(request, 'Account created Successfully for: ' + username)
      return redirect('register')

  context = {'form': form, 'groups': groups}
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


@login_required(login_url='login')
def dashboard(request):
  return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def usersList(request):
  users = User.objects.all()
  context = {'users': users}
  return render(request, 'accounts/users-list.html', context)