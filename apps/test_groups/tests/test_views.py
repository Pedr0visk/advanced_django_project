from datetime import date

from django.test import TestCase, Client
from django.contrib.auth.models import Group, User
from django.urls import reverse

from ..models import TestGroup
from apps.bops.models import Bop
from apps.failuremodes.models import FailureMode

from ...components.models import Component
from ...subsystems.models import Subsystem


class TestGroupViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # for the tests purpose will be needed 3 types of groups
        operator_group = Group.objects.create(name='Operator')

        cls.user = User.objects.create_user(username='peter', password='passw0rd123')
        cls.user.groups.add(operator_group)

        cls.b1 = Bop.objects.create(name='bop 1')
        cls.b2 = Bop.objects.create(name='bop 2')

        cls.s1 = Subsystem.objects.create(name='sub 1', code='FSS_1', bop=cls.b1)
        cls.s2 = Subsystem.objects.create(name='sub 2', code='FSS_2', bop=cls.b1)
        cls.s3 = Subsystem.objects.create(name='sub 2', code='FSS_2', bop=cls.b2)

        cls.c1 = Component.objects.create(name='comp 1', code='C_1', subsystem=cls.s1)
        cls.c2 = Component.objects.create(name='comp 2', code='C_2', subsystem=cls.s1)
        cls.c3 = Component.objects.create(name='comp 3', code='C_3', subsystem=cls.s2)
        cls.c4 = Component.objects.create(name='comp 4', code='C_4', subsystem=cls.s2)
        cls.c5 = Component.objects.create(name='comp 1', code='C_1', subsystem=cls.s3)

        cls.fm1 = FailureMode.objects.create(name='failure mode 1',
                                             diagnostic_coverage=1,
                                             distribution='',
                                             code='FM_1',
                                             component=cls.c1)
        cls.fm2 = FailureMode.objects.create(name='failure mode 2',
                                             diagnostic_coverage=1,
                                             distribution='',
                                             code='FM_2',
                                             component=cls.c2)
        cls.fm3 = FailureMode.objects.create(name='failure mode 3',
                                             diagnostic_coverage=1,
                                             distribution='',
                                             code='FM_3',
                                             component=cls.c3)
        cls.fm4 = FailureMode.objects.create(name='failure mode 4',
                                             diagnostic_coverage=1,
                                             distribution='',
                                             code='FM_4',
                                             component=cls.c4)
        cls.fm5 = FailureMode.objects.create(name='failure mode 1',
                                             diagnostic_coverage=1,
                                             distribution='',
                                             code='FM_1',
                                             component=cls.c5)

        cls.tg1 = TestGroup.objects.create(bop=cls.b1,
                                           start_date='2020-12-01',
                                           tests='[{"coverage": 1, "interval": 336}]')
        cls.tg1.failure_modes.set([cls.fm2, cls.fm4])

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.create_url = f'/bops/{self.b1.pk}/test-groups/add/'
        self.update_url = f'/bops/{self.b1.pk}/test-groups/{self.tg1.pk}/change/'

    def test_create_test_group(self):
        response = self.client.post(self.create_url, self.data())

        tg = TestGroup.objects.get(pk=2)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('2020-08-31', tg.start_date.__str__())
        self.assertEqual(2, TestGroup.objects.count())
        self.assertJSONEqual('[{"coverage": 1, "interval": 168}]', tg.tests)

    def test_update_test_group(self):
        response = self.client.post(self.update_url, self.data())

        tg = TestGroup.objects.get(pk=self.tg1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, TestGroup.objects.count())
        self.assertJSONEqual('[{"coverage": 1, "interval": 168}]', tg.tests)
        self.assertEqual('2020-08-31', tg.start_date.__str__())
        self.assertEquals(tg.failure_modes.count(), 3)

    @staticmethod
    def data():
        return {
            'start_date': '2020-08-31',
            'tests': '[{"coverage": 1, "interval": 168}]',
            'failure_modes': [1, 3, 4]
        }
