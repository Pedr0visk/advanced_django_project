from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect 

from django.contrib import messages

def allowed_users(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None 
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name 

      print('grupo', group)
      if group in allowed_roles:
        return view_func(request, *args, **kwargs)
      else: 
        messages.info(request, "You are logged but you are not Admin, try to log in with another account")
        url = '/manager/login/?next='+request.path
        return HttpResponseRedirect(url)
    return wrapper_func
  return decorator
  