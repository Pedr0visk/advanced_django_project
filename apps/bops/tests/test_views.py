from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop

from apps.campaigns.models import Campaign


class BopViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # for the tests puporse will be needed 3 types of groups
        operator_group = Group.objects.create(name='Operator')

        self.user = User.objects.create_user(username='peter', password='passw0rd123')
        self.user.groups.add(operator_group)

        # pk was applied cause the test was creating two bops and getting the test to red
        self.bop = Bop.objects.create(pk=1, name='first bop')
        Campaign.objects.create(bop=self.bop, name='first campaign')

    def test_list_bop_campaigns(self):

        """
        Assert 200 for bop campaigns list
        """
        self.client.force_login(self.user)

        """
        the param pk is 1 cause we have just one bop created on database
        """
        response = self.client.get('/bops/1/campaigns/')

        self.assertEquals(response.status_code, 200)

    def test_campaign_can_be_created_by_operator(self):
        """
        A campaign can be created for a bop
        """
        self.client.force_login(self.user)

        """
        the param pk is 1 cause we have just one bop created on database
        """
        data = self.campaign_data()
        response = self.client.post('/bops/1/campaigns/add/', data)

        self.assertRedirects(response, '/bops/1/campaigns/')
        self.assertEquals(Campaign.objects.count(), 2)


    def test_campaign_can_be_created_without_description(self):
        """
        A campaign can be created for a bop
        """
        self.client.force_login(self.user)

        """
        the param pk is 1 cause we have just one bop created on database
        """
        data = self.campaign_data()
        data['description'] = ''
        response = self.client.post('/bops/1/campaigns/add/', data)

        self.assertRedirects(response, '/bops/1/campaigns/')
        self.assertEquals(Campaign.objects.count(), 2)

    @staticmethod
    def campaign_data():
        """
        Private function that returns data for user creation
        """
        return {
            'name': 'first campaign',
            'description': 'some short description',
            'status': 'Green',
            'well_name': 'well 1',
            'rig_name': 'rig 1',
            'active': False
        }
