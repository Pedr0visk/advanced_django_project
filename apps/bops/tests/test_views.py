import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop, Rig, SafetyFunction
from apps.certifications.models import Certification
from apps.components.models import Component
from apps.failuremodes.models import FailureMode
from apps.subsystems.models import Subsystem
from apps.test_groups.models import TestGroup, TestGroupDummy


class BopViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        operator_group = Group.objects.create(name='Admin')

        cls.user = User.objects.create_user(username='peter', password='passw0rd123')
        cls.user.groups.add(operator_group)

        cls.rig = Rig.objects.create(name='first rig')
        cls.bop = Bop.objects.create(name='han solo')

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

        bop_id = self.bop.id
        self.bop_create_url = reverse('upload_bop')
        self.bop_index_url = f'/bops/{bop_id}/'
        self.bop_update_url = f'/bops/{bop_id}/change/'
        self.bop_delete_url = f'/bops/{bop_id}/delete/'

        self.safety_function_create_url = f'/bops/{bop_id}/safety-functions/upload/'
        self.safety_function_delete_url = lambda url: f'/bops/{self.bop.pk}/safety-functions/{url}/delete/'

        self.test_planner_create_url_get = f'/bops/{self.b1.pk}/test-planner/'
        self.test_planner_create_url_post = f'/bops/{self.b1.pk}/test-groups/add/'

        self.client.get(self.test_planner_create_url_get)
        self.tgd1 = TestGroupDummy.objects.first()

        self.test_planner_update_url_post = f'/bops/{self.b1.pk}/test-groups/{self.tgd1.pk}/change/'
        self.test_planner_delete_url_post = f'/bops/{self.b1.pk}/test-groups/{self.tgd1.pk}/delete/'

        self.migrate_url_get = f'/bops/{self.b1.pk}/test-planner/raw/migrate/'

    # Tests for Bop
    def test_create_bop(self):
        _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/bopfile.txt')

        with open(_path) as file:
            data = self.bop_data()
            data['file'] = file
            response = self.client.post(self.bop_create_url, data)

        bop = Bop.objects.get(name='Darth Vader')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bop.objects.count(), 4)
        self.assertEqual(bop.subsystems.count(), 45)
        self.assertEqual(Component.objects.count(), 158)
        self.assertEqual(FailureMode.objects.count(), 163)
        self.assertEqual(Certification.objects.count(), 1)

    def test_load_bop(self):
        _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/bopfile.txt')

        for _ in range(2):
            with open(_path) as file:
                data = self.bop_data()
                data['file'] = file
                self.client.post(self.bop_create_url, data)

        self.assertEqual(Bop.objects.count(), 5)
        self.assertEqual(Subsystem.objects.count(), 93)
        self.assertEqual(FailureMode.objects.count(), 321)

    def test_create_bop_without_text_file(self):
        """
        In setup data we have 5 components and failure modes created
        :return:
        """
        response = self.client.post(self.bop_create_url, self.bop_data())

        bop = Bop.objects.get(name='Darth Vader')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bop.objects.count(), 4)
        self.assertEqual(bop.subsystems.count(), 0)
        self.assertEqual(Component.objects.count(), 5)
        self.assertEqual(FailureMode.objects.count(), 5)
        self.assertEqual(Certification.objects.count(), 1)

    def test_update_bop(self):
        response = self.client.post(self.bop_update_url, {'name': 'han solo updated', 'rig': self.rig.id})

        bop = Bop.objects.get(pk=self.bop.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(bop.name, 'han solo updated')

    def test_bop_update_form_invalid(self):
        response = self.client.post(self.bop_update_url, {'name': 'han solo updated'})

        bop = Bop.objects.get(pk=self.bop.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bop.name, 'han solo')

    def test_bop_delete(self):
        response = self.client.post(self.bop_delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bop.objects.count(), 2)

    def test_create_safety_function(self):
        __dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(__dir, 'assets/bopfile.txt')
        with open(file_path) as file:
            data = self.bop_data()
            data['file'] = file
            self.client.post(self.bop_create_url, data)

        file_path = os.path.join(__dir, 'assets/SF-1.txt')
        with open(file_path) as file:
            data = self.safety_function_data()
            data['file'] = file
            response = self.client.post(self.safety_function_create_url, data)

        sf = SafetyFunction.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(SafetyFunction.objects.count(), 1)
        self.assertEqual(sf.cuts.count(), 2759)

    def test_delete_safety_function(self):
        sf = SafetyFunction.objects.create(bop=self.bop, name='SF-2', description='some short desc')
        response = self.client.post(self.safety_function_delete_url(sf.pk))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(SafetyFunction.objects.count(), 0)

    # Tests for Test Group
    def test_list_test_group(self):
        """
        When user access this page, the system should
        create an mirror of test group table called test_group_dummy table
        :return:
        """
        self.client.get(self.test_planner_create_url_get)

        self.assertEqual(TestGroupDummy.objects.count(), 1)

    def test_create_test_group_dummy(self):
        """
        Create an instance of test_group_dummy instead of test_group
        :return:
        """
        response = self.client.post(self.test_planner_create_url_post, self.test_group_data())

        tgd = TestGroupDummy.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertEqual('2020-08-31', tgd.start_date.__str__())
        self.assertEqual(2, TestGroupDummy.objects.count())
        self.assertEqual(1, TestGroup.objects.count())
        self.assertJSONEqual('[{"coverage": 1, "interval": 168}]', tgd.tests)

    def test_update_test_group_dummy(self):
        """
        Update an clone of test_group in test_group_dummy table
        :return:
        """
        response = self.client.post(self.test_planner_update_url_post, self.test_group_data())

        tg = TestGroupDummy.objects.get(pk=self.tgd1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, TestGroup.objects.count())
        self.assertEqual(1, TestGroupDummy.objects.count())
        self.assertJSONEqual('[{"coverage": 1, "interval": 168}]', tg.tests)
        self.assertEqual('2020-08-31', tg.start_date.__str__())
        self.assertEquals(tg.failure_modes.count(), 3)

    def test_delete_test_group_dummy(self):
        """
        Delete a clone created for a instance of test_group on test_group_dummy table
        :return:
        """
        response = self.client.post(self.test_planner_delete_url_post)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, TestGroup.objects.count())
        self.assertEqual(0, TestGroupDummy.objects.count())

    def test_migrate_test_group_dummy(self):
        self.client.post(self.test_planner_create_url_post, self.test_group_data())
        self.client.post(self.test_planner_create_url_post, self.test_group_data())
        self.client.get(self.migrate_url_get)

        self.assertEqual(3, TestGroupDummy.objects.count())
        self.assertEqual(3, TestGroup.objects.count())

    @staticmethod
    def bop_data():
        return {
            'rig': 1,
            'name': 'Darth Vader',
            'file': '',
            'code': 'XSLR02',
            'start_date': '2020-01-09',
            'end_date': '2020-01-09',
        }

    @staticmethod
    def safety_function_data():
        return {
            'name': 'sf 1',
            'description': 'some description',
            'file': ''
        }

    @staticmethod
    def test_group_data():
        return {
            'start_date': '2020-08-31',
            'tests': '[{"coverage": 1, "interval": 168}]',
            'failure_modes': [1, 3, 4]
        }
