import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop
from apps.campaigns.models import Campaign


class CampaignViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # for the tests puporse will be needed 3 types of groups
        operator_group = Group.objects.create(name='Operator')

        self.user = User.objects.create_user(username='peter', password='passw0rd123')
        self.user.groups.add(operator_group)

        # pk was applied cause the test was creating two bops and getting the test to red
        self.bop = Bop.objects.create(pk=1, name='first bop')
        self.campaign = Campaign.objects.create(pk=6, bop=self.bop, name='first campaign')

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

    def test_campaign_can_be_created_with_blank_description(self):
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

    def test_campaign_can_be_created_with_blank_period(self):
        """
        A campaign can be created for a bop
        with start_date and end_date set to null or ''
        """
        self.client.force_login(self.user)

        """
        the param pk is 1 cause we have just one bop created on database
        """
        data = self.campaign_data()
        data['start_date'] = ''
        data['end_date'] = ''
        response = self.client.post('/bops/1/campaigns/add/', data)

        self.assertRedirects(response, '/bops/1/campaigns/')
        self.assertEquals(Campaign.objects.count(), 2)

    def test_campaign_can_be_get_for_edit(self):
        """
        Tests if a campaign can be displayed for a update
        """
        self.client.force_login(self.user)

        response = self.client.get('/bops/1/campaigns/{}/change/'.format(self.campaign.pk))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('campaigns/campaign_form.html')

    def test_campaign_can_be_updated(self):
        """"""
        self.client.force_login(self.user)

        data = self.campaign_data()
        data['name'] = 'Campaign 1 edited'
        data['start_date'] = '2020-08-31'

        response = self.client.post('/bops/1/campaigns/{}/change/'.format(self.campaign.pk), data)

        self.assertRedirects(response, '/bops/1/campaigns/')

        updated_campaign = Campaign.objects.get(pk=self.campaign.pk)

        self.assertEquals(updated_campaign.name, data['name'])
        self.assertEquals(updated_campaign.active, False)
        self.assertEquals(updated_campaign.start_date.isoformat(), data['start_date'])

    @staticmethod
    def campaign_data():
        """
        Private function that returns data for user creation
        """
        return {
            'name': 'first campaign',
            'description': 'some short description',
            'well_name': 'well 1',
            'active': False,
            'start_date': '2020-08-01',
            'end_date': '2020-12-31',
        }
