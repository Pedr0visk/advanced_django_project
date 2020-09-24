from django.test import TestCase, Client
from django.contrib.auth.models import Group, User
from django.urls import reverse

from ..models import TestGroup, TestGroupDummy
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

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)




    @staticmethod
    def test_group_data():
        return {
            'start_date': '2020-08-31',
            'tests': '[{"coverage": 1, "interval": 168}]',
            'failure_modes': [1, 3, 4]
        }
