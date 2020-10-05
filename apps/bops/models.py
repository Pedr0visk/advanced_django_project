from django.db import models
from django.contrib.admin.utils import NestedObjects
from django.db import connection
from django.urls import reverse


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

    def success_url(self):
        return reverse('bops:index', args=[self.pk])

    def get_absolut_url(self):
        from django.urls import reverse
        return reverse('apps.bops.views.index', args=[str(self.pk)])

    def last_certification(self):
        return self.certifications.last()

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
        return model_count.items()

    def schedule_tests(self, start_date, *args, **kwargs):
        print(self.testgroup.all())
        print(**kwargs)


class SafetyFunction(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name="safety_functions")

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
        return model_count.items()

    def success_url(self):
        return reverse('bops:list_safety_functions', args=[self.bop.pk])

    def __str__(self):
        return self.name
