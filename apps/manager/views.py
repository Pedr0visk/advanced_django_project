from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Guest'])
def dashboard(request):
  return render(request, 'manager/dashboard.html')

@allowed_users(allowed_roles=['Admin', 'Guest'])
def accounts_list(request):
  return HttpResponse('Accounts list')


def login_page(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    redirect_url = request.GET.get('next')
    print('manager')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      # in case of next param in url
      if redirect_url is not None:
        return redirect(redirect_url)

      # else redirect to the dashboard
      login(request, user)
      return redirect('dashboard')
    else:
      messages.info(request, "username or email is incorrect")

  context = {}
  return render(request, 'manager/login.html', context)