from django.db import models
from apps.bops.models import SafetyFunction
from apps.failuremodes.models import FailureMode
from functools import reduce

from django.core.cache import cache


class Cut(models.Model):
    index = models.BigIntegerField()
    order = models.BigIntegerField()
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    safety_function = models.ForeignKey(SafetyFunction,
                                        on_delete=models.CASCADE,
                                        related_name='cuts')

    failure_modes = models.ManyToManyField(FailureMode)

    def pfd(self, step):
        """
        P(C1) = P {1, 2} = P(1)*P(2)

        list = self.failure_modes.all() # [fm1, fm2, fm3]


        return 1 - (1 - reduce(lambda x.calculate_pfd(), y.calculate_pfd(): x*y), list)
        """
        results = []

        if cache.get('failuremodes'):
            fm_set = cache.get('failuremodes')

            for fm in self.failure_modes.all():
                results.append(fm_set[step][fm.code])

            return 1 - (1 - reduce((lambda x, y: x * y), results))
