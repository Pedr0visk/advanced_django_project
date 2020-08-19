from django.db import models


class Bop(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subsystem(models.Model):
    code = models.CharField(max_length=50, unique=True)
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE, related_name='subsystems')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Component(models.Model):
    code = models.CharField(max_length=50, unique=True)
    subsystem = models.ForeignKey(Subsystem, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FailureMode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='failures_mode')
    failure_mode = models.ForeignKey('self', on_delete=models.PROTECT, related_name='failure_children')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SafetyFunction(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Cut(models.Model):
    safety_function = models.ForeignKey(SafetyFunction, on_delete=models.CASCADE)
    failures_mode = models.TextField()

