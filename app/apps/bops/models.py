from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.admin.utils import NestedObjects
from django.urls import reverse


class Bop(models.Model):
    name = models.CharField(max_length=100)
    rig = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    matrix = JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def success_url(self):
        return reverse('bops:index', args=[self.pk])

    def get_absolut_url(self):
        from django.urls import reverse
        return reverse('bops:index', args=[str(self.pk)])

    def get_last_certification(self):
        print('[LOG]', self.certifications.last())
        return self.certifications.last()

    def active_campaign(self):
        return self.campaigns.filter(active=True).first()

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(
            objs) for model, objs in collector.model_objs.items()}
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
        subsystem_qs = self.subsystems.prefetch_related(
            'components__failure_modes').order_by('code')
        failure_modes = []
        for subsystem in subsystem_qs:
            for component in subsystem.components.all():
                failure_modes += component.failure_modes.all()

        failure_modes.sort(key=lambda item: item.code)
        return failure_modes

    @staticmethod
    def get_matrix(bop):
        def gerar_matriz(n_linhas, n_colunas):
            return [[0] * n_colunas for _ in range(n_linhas)]

        failure_modes = bop.failure_modes
        print('all fms', len(failure_modes))
        m = gerar_matriz(len(failure_modes), 32)

        index = 0
        for f in failure_modes:
            m[index][0] = index

            if f.component is not None:
                cp = f.component
                m[index][4] = cp.name
                m[index][5] = cp.code
                # m[index][22] = f.Last_Replacement_Date
                m[index][22] = 0
                bs = cp.subsystem
                m[index][2] = bs.name
                m[index][3] = bs.code
            else:
                m[index][2] = "CCF"
                m[index][3] = "CCF"
                m[index][4] = "CCF"
                m[index][5] = "CCF"

                # ccfs = ""
                # for m in f.ccf_impacted.all():
                #    fm = BopFailureMode.objects.get(pk=m.id)
                #    if len(ccfs) != 0:
                #        ccfs += ","
                #    ccfs += fm.code

            # m[index][9] = f.ccf_impacted
            # print("f", f.ccf_impacted)

            # if m[index][9]:
            #    m[index][9] = modefail(m[index][9])

            m[index][6] = f.name
            m[index][7] = f.code
            m[index][8] = f.code
            m[index][10] = 168

            #     if f.test_interval_1 == None:
            #         m[index][10] = 0
            #    else:
            #       m[index][10] = f.test_interval_1 / 24

            #   if f.test_interval_2 == None:
            ###      m[index][11] = 0
            #    else:
            #      m[index][11] = f.test_interval_2 / 24

            #   if f.test_interval_3 == None:
            #       m[index][12] = 0
            #   else:
            #       m[index][12] = f.test_interval_3 / 24

            #   if f.test_interval_4 == None:
            #       m[index][13] = 0
            #   else:
            #       m[index][13] = f.test_interval_4 / 24

            m[index][14] = f.diagnostic_coverage
            m[index][15] = 1
            # m[index][15] = f.test_coverage_1
            # m[index][16] = f.test_coverage_2
            # m[index][17] = f.test_coverage_3
            # m[index][18] = f.test_coverage_4

            if m[index][19] == None:
                m[index][19] = 0
            else:
                # m[index][19] = f.staggering_Test_Time_t0
                m[index][19] = 0
            # if f.repairable_with_BOP_Installed:
            #   m[index][20] = "x"
            # else:
            m[index][20] = ""

            # if f.mean_time_to_restoration == None:
            m[index][21] = 0
            # else:
            #   m[index][21] = f.mean_time_to_restoration / 24
            dist = f.distribution

            m[index][23] = dist['type']
            if m[index][23] == 'Exponential':
                m[index][24] = dist['exponential_failure_rate']

            elif m[index][23] == 'Probability':
                m[index][31] = dist['probability']

            elif m[index][23] == 'Weibull':
                m[index][25] = dist['scale']
                m[index][26] = dist['form']

            elif m[index][23] == 'Step':
                dist['cycle'] = {}
                m[index][27] = dist['initial_failure_rate']
                m[index][28] = dist['value']
                m[index][29] = 0
                m[index][30] = 0

            index += 1

        return m


class SafetyFunction(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    bop = models.ForeignKey(Bop,
                            on_delete=models.CASCADE,
                            related_name="safety_functions")

    def with_counts(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        model_count = {model._meta.verbose_name_plural: len(
            objs) for model, objs in collector.model_objs.items()}
        return model_count.items()

    def success_url(self):
        return reverse('bops:list_safety_functions', args=[self.bop.pk])

    def __str__(self):
        return self.name


class Certification(models.Model):
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE,
                            related_name='certifications')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'certification {self.id}'
