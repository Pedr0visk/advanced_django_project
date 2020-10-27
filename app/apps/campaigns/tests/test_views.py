import datetime

from django.core.serializers import json
from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

from apps.bops.models import Bop
from apps.campaigns.models import Campaign, Phase


class CampaignViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # for the tests purpose will be needed 3 types of groups
        operator_group = Group.objects.create(name='Operator')

        cls.user = User.objects.create_user(username='peter', password='passw0rd123')
        cls.user.groups.add(operator_group)

        # pk was applied cause the test was creating two bops and getting the test to red
        cls.bop = Bop.objects.create(pk=1, name='first bop')
        cls.campaign = Campaign.objects.create(bop=cls.bop, name='first campaign')

    def setUp(self):
        self.client.force_login(self.user)

    def test_campaign_can_be_created_along_with_phases(self):
        """
        A campaign must have schemas on it, it will be created via ajax using
        an api endpoint
        """
        data = self.campaign_data()
        response = self.client.post('/bops/1/campaigns/add/', data)

        c = Campaign.objects.get(name=data['name'])

        self.assertRedirects(response, '/bops/1/campaigns/')
        self.assertEquals(Campaign.objects.count(), 2)
        self.assertEquals(c.name, data['name'])
        self.assertEquals(c.phases.count(), 4)

    def test_campaign_can_be_created_with_blank_description(self):
        """
        A campaign can be created for a bop
        """

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

        response = self.client.get('/bops/1/campaigns/{}/change/'.format(self.campaign.pk))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('campaigns/campaign_form.html')

    def test_campaign_can_be_updated(self):
        """"""

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
            'name': 'stargazing',
            'description': 'some short description',
            'well_name': 'well 1',
            'active': False,
            'start_date': '2020-08-01',
            'end_date': '2020-12-31',
            'schemas': json.dumps([
                {
                    'name': 'Descend phase',
                    'start_date': '2020-08-01',
                    'duration': 45.7,
                    'step': 1,
                },
                {
                    'name': 'Connection test phase',
                    'start_date': '2020-08-03',
                    'duration': 30,
                    'step': 2,
                },
                {
                    'name': '1 drilling phase',
                    'start_date': '2020-08-03',
                    'duration': 467,
                    'step': 3
                },
                {
                    'name': 'Disconnect phase',
                    'start_date': '2020-09-01',
                    'duration': 80,
                    'step': 4,
                }
            ])
        }
