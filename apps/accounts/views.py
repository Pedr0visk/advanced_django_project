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


@allowed_users(allowed_roles=['Admin', 'Guest'])
def register_page(request):

  form = CreateUserForm()
  groups = Group.objects.all()

  if request.method == 'POST':
    # extends the UserCreateForm
    form = CreateUserForm(request.POST)
    if form.is_valid():
      group = Group.objects.get(name=request.POST['group'])
      # create user on database
      user = form.save()
      user.groups.add(group)

      Employer.objects.create(user=user,)

      # create message of success
      username = form.cleaned_data.get('username')
      messages.success(request, 'Account created Successfully for: ' + username)

      return redirect('register')

  context = {'form': form, 'groups': groups}
  return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
  print('accounts')
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Guest'])
def users_list(request):
  users = User.objects.all()
  context = {'users': users}
  return render(request, 'accounts/users-list.html', context)