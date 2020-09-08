import re
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
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name="safety_functions")

    def __str__(self):
        return self.name

    def calculate_probability(self, step):
        p = 1
        """
        P(C1 U C2 ... CN) = 1 - (1 - P(C2))*(1-P(C3))

        return 1 - reduce(lambda x, y: x*y))

        """
        pass

    def reduce(self, failed_failure_mode):
        pass
        """
            ### armazenamento
            ### busca

            #1. Separar cuts por ordem
            #2. buscar modulo de falha em cada corte
            #3. promover corte para um nova ordem
            #4. remover cortes que possuam um modulo de falha dos cortes promovidos


            high_order_cuts = self.cuts.filter(order=1)
            medium_order_cuts = self.cuts.filter(order=2)
            lower_order_cuts = self.cuts.filter(order=3)

            promoted_failure_modes = [] # 'AB_CD', 'EF_GH', 'IJ_KL'

            for cut in medium_order_cuts:
                failure_mode = cut.upgrade(failed_failure_mode)
                promoted_failure_modes.append(failure_mode)

        """


class Test(models.Model):
    interval = models.FloatField()
    coverage = models.FloatField()

    def __str__(self):
        return f'interval: {self.interval!r} - coverage: {self.coverage!r}'


class TestGroup(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    code = models.BigIntegerField(unique=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    tests = models.ManyToManyField(Test, related_name='groups')

    def __str__(self):
        return str(self.code)
