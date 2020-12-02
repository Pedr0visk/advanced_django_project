from django.db import models
from django.contrib.admin.utils import NestedObjects
from django.urls import reverse



class Bop(models.Model):
    name = models.CharField(max_length=100)
    rig = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

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

    def active_campaign(self):
        return self.campaigns.filter(active=True).first()

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
        return model_count.items()

    def schedule_tests(self, start_date, *args, **kwargs):
        print(self.testgroup.all())
        print(**kwargs)

    @property
    def components(self):
        subsystem_qs = self.subsystems.prefetch_related('components')
        components = []
        for subsystem in subsystem_qs:
            components += subsystem.components.all()

        components.sort(key=lambda item: item.code)
        return components

    @property
    def failure_modes(self):
        subsystem_qs = self.subsystems.prefetch_related('components__failure_modes').order_by('code')
        failure_modes = []
        for subsystem in subsystem_qs:
            for component in subsystem.components.all():
                failure_modes += component.failure_modes.all()

        failure_modes.sort(key=lambda item: item.code)
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
