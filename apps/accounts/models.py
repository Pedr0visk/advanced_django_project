from django.db import models
from django.contrib.auth.models import User 

class Employer(models.Model):
  user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.user.username