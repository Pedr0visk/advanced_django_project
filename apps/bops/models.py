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


class Certification(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name="certifications")

    def __str__(self):
        return '{0} {1} certification'.format(self.pk, self.bop.name)


class SafetyFunction(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Cut(models.Model):
    safety_function = models.ForeignKey(SafetyFunction, on_delete=models.CASCADE)
    failures_mode = models.TextField()


class Test(models.Model):
    interval = models.FloatField()
    coverage = models.FloatField()


class TestGroup(models.Model):
    name = models.CharField(max_length=50)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    tests = models.ManyToManyField(Test, related_name='groups')

    def __str__(self):
        return self.name
