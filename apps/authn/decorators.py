from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect 

from django.contrib import messages

def unauthenticated_user(view_func):
  def wrapper_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('dashboard')
    else:
      return view_func(request, *args, **kwargs)
      
  return wrapper_func

def allowed_users(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None 
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name 

      if group in allowed_roles:
        return view_func(request, *args, **kwargs)
      else: 
        messages.info(request, "You are logged but you are not Admin, try to log in with another account")
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return wrapper_func
  return decorator
  