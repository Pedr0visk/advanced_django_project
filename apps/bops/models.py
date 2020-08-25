from django.db import models


class Rig(models.Model):
    name = models.CharField(max_length=100)


class Bop(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=100)
    rig = models.ForeignKey(Rig,
                            on_delete=models.PROTECT,
                            null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Certification(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name="certifications")

    def __str__(self):
        return '{} {} certification'.format(self.pk, self.bop.name)


class Subsystem(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name='subsystems')

    def __str__(self):
        return self.name


class Component(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    subsystem = models.ForeignKey(Subsystem, on_delete=models.CASCADE, related_name='components')

    def __str__(self):
        return self.name


class FailureMode(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='failures_mode')
    failure_mode = models.ForeignKey('self', on_delete=models.PROTECT, related_name='failure_children')

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
