from functools import reduce
from django.db import models


class Rig(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bop(models.Model):
    name = models.CharField(max_length=100)
    rig = models.ForeignKey(Rig,
                            on_delete=models.PROTECT,
                            null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SafetyFunction(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name="safety_functions")

    def __str__(self):
        return self.name
