from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop

from apps.campaigns.models import Campaign


class BopViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        operator_group = Group.objects.create(name='Operator')

        cls.user = User.objects.create_user(username='peter', password='passw0rd123')
        cls.user.groups.add(operator_group)

        cls.bop = Bop.objects.create(name='first bop')

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.migrate_url = reverse('test_planner_migrate', self.bop.pk)
