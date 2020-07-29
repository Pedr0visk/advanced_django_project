from django.db import models

class Bop(models.Model):
  code = models.CharField(max_length=8)
  name = models.CharField(max_length=100)
  description = models.TextField(null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self):
    return self.name + " " + self.code