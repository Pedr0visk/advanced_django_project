import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop, Rig
from apps.certifications.models import Certification
from apps.components.models import Component
from apps.failuremodes.models import FailureMode


class BopViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        operator_group = Group.objects.create(name='Admin')

        cls.user = User.objects.create_user(username='peter', password='passw0rd123')
        cls.user.groups.add(operator_group)

        cls.rig = Rig.objects.create(name='first rig')

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.create_url = reverse('upload_bop')

    def test_create_bop(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/bopfile.txt')) as file:
            response = self.client.post(self.create_url, {
                'rig': self.rig.id,
                'name': 'first bop',
                'attachment': file,
                'code': 'XSLR02',
                'start_date': '2020-01-09',
                'end_date': '2020-01-09',
            })

        bop = Bop.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bop.objects.count(), 1)
        self.assertEqual(bop.subsystems.count(), 45)
        self.assertEqual(bop.name, 'first bop')
        self.assertEqual(Component.objects.count(), 153)
        self.assertEqual(FailureMode.objects.count(), 158)
        self.assertEqual(Certification.objects.count(), 1)

    @staticmethod
    def data():
        return {'name': 'first bop'}
