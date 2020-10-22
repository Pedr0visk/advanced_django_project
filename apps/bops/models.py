from django.db import models
from django.contrib.admin.utils import NestedObjects
from django.urls import reverse
from .decorators import query_debugger


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

    @query_debugger
    def component_list(self):
        subsystem_qs = self.subsystems.prefetch_related('components').all()
        components = []
        for subsystem in subsystem_qs:
            components += subsystem.components.all()

        return components

    @query_debugger
    def failure_mode_list(self):
        subsystem_qs = self.subsystems.prefetch_related('components__failure_modes').all()
        failure_modes = []
        for subsystem in subsystem_qs:
            for component in subsystem.components.all():
                failure_modes += component.failure_mode_list()

        return failure_modes


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
