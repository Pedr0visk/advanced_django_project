from django.db import models
from apps.bops.models import Bop


class Subsystem(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name='subsystems')
    slug = models.SlugField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('code', 'name',)

    def save(self, *args, **kwargs):
        self.slug = self.code.lower().replace('_', '-')
        super(Subsystem, self).save(*args, **kwargs)

    def component_list(self):
        return self.components.all()

    def __str__(self):
        return self.name
