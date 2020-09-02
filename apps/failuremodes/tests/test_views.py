from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop
from apps.subsystems.models import Subsystem
from apps.components.models import Component
from apps.failuremodes.models import FailureMode


class CampaignViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # for the tests puporse will be needed 3 types of groups
        operator_group = Group.objects.create(name='Operator')

        cls.user = User.objects.create_user(username='peter', password='passw0rd123')
        cls.user.groups.add(operator_group)

        # pk was applied cause the test was creating two bops and getting the test to red
        cls.bop = Bop.objects.create(pk=1, name='first bop')
        cls.subsystem = Subsystem.objects.create(name='subsystem 1',
                                                 code='SS_1',
                                                 bop=cls.bop, )

        cls.component = Component.objects.create(name='component 1',
                                                 code='CC_1',
                                                 subsystem=cls.subsystem)

        cls.fm1 = FailureMode.objects.create(code='UPR_SV2_FTO_NO_CCF',
                                             name='UPR Shuttle Valve SV2 Modular PODs fails to open',
                                             component=cls.component,
                                             diagnostic_coverage=1,
                                             distribution={'type': 'Exponential',
                                                           'exponential_failure_rate': 2.3})

        cls.fm2 = FailureMode.objects.create(code='ULPR_SV2_CCF',
                                             name='UPR and LPR Shuttle Valves SV2 common cause failures',
                                             component=cls.component,
                                             diagnostic_coverage=1,
                                             distribution={'type': 'Probability',
                                                           'probability': '2.09E-07'})

        cls.fm3 = FailureMode.objects.create(code='UAP_SV_FTO_NO_CCF',
                                             name='UAP Shuttle Valve SV Modular PODs fails to open',
                                             component=cls.component,
                                             diagnostic_coverage=1,
                                             distribution={'type': 'Step',
                                                           'initial_failure_rate': '3.8E-05',
                                                           'cycle': {
                                                               'limit': 5,
                                                               'size': 336,
                                                               'value': 0.2
                                                           }})

        cls.fm4 = FailureMode.objects.create(code='LAP_SV_FTO_NO_CCF',
                                             name='UPR Shuttle Valve SV2 Modular PODs fails to open edited',
                                             component=cls.component,
                                             diagnostic_coverage=1,
                                             distribution={'type': 'Weibull',
                                                           'scale': 25000,
                                                           'form': 1.4})

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_can_edit_failure_mode_of_type_exponential(self):
        data = {
            'name': 'UPR Shuttle Valve SV2 Modular PODs fails to open edited',
            'component': self.component.pk,
            'diagnostic_coverage': 1.4,
            'distribution': '{"type": "Exponential", "exponential_failure_rate": 0.4}'
        }

        response = self.client.post('/bops/{0}/failuremodes/{1}/change/'.format(self.bop.pk, self.fm1.pk), data)

        fm = FailureMode.objects.get(pk=self.fm1.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(fm.diagnostic_coverage, 1.4)
        self.assertEquals(fm.distribution['exponential_failure_rate'], 0.4)
        self.assertEquals(fm.name, 'UPR Shuttle Valve SV2 Modular PODs fails to open edited')

    def test_can_edit_failure_mode_of_type_probability(self):
        data = {
            'name': 'UPR Shuttle Valve SV2 Modular PODs fails to open edited',
            'component': self.component.pk,
            'diagnostic_coverage': 1.3,
            'distribution': '{"type": "Probability", "probability": 0.5}'
        }

        response = self.client.post('/bops/{0}/failuremodes/{1}/change/'.format(self.bop.pk, self.fm2.pk), data)

        fm = FailureMode.objects.get(pk=self.fm2.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(fm.diagnostic_coverage, 1.3)

    def test_can_edit_failure_mode_of_type_step(self):
        data = {
            'name': 'UPR Shuttle Valve SV2 Modular PODs fails to open edited',
            'component': self.component.pk,
            'diagnostic_coverage': 1.3,
            'distribution': '{\
                "type": "step",\
                "diagnostic_coverage": 0.45,\
                "initial_failure_rate": "1.8E-05",\
                "cycle": {\
                    "size": 122,\
                    "limit": 3,\
                    "value": 0.5\
                }\
            }'
        }

        response = self.client.post('/bops/{0}/failuremodes/{1}/change/'.format(self.bop.pk, self.fm3.pk), data)

        fm = FailureMode.objects.get(pk=self.fm3.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(fm.diagnostic_coverage, 1.3)

    def test_can_edit_failure_mode_of_type_weilbull(self):
        data = {
            'name': 'LAP Shuttle edited',
            'component': self.component.pk,
            'diagnostic_coverage': 0.32,
            'distribution': '{"type": "Probability", "form": 1.6, "scale": 1800}'
        }

        response = self.client.post('/bops/{0}/failuremodes/{1}/change/'.format(self.bop.pk, self.fm4.pk), data)

        fm = FailureMode.objects.get(pk=self.fm4.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(fm.name, 'LAP Shuttle edited')
        self.assertEquals(fm.diagnostic_coverage, 0.32)
        self.assertEquals(fm.distribution['scale'], 1800)
        self.assertEquals(fm.distribution['form'], 1.6)
