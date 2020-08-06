from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import CreateUserForm
from .decorators import allowed_users, unauthenticated_user
from apps.accounts.models import Employer

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
  return render(request, 'authn/register.html', context)
  

@unauthenticated_user
def login_page(request):
  """
  This login method checks if exists an user set on the request
  if so, this method log the user out and log in another user
  """
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    redirect_url = request.GET.get('next')

    if request.user is not None:
      logout(request)
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)

      # in case of next param in url
      if redirect_url is not None:
        return HttpResponseRedirect(redirect_url)
      else:
        return reverse('dashboard')
    else:
      messages.info(request, "username or email is incorrect")

  context = {}
  return render(request, 'authn/login.html', context)


def logout_user(request):
  logout(request)
  return redirect('login')
