from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User


class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Defaults urls
        self.update_profile_url = reverse('update_profile')
        self.password_change_url = reverse('password_change')

        # Setup group for user
        operator_group = Group.objects.create(name='Operator')

        # Create new user for tests
        self.user = User.objects.create_user(username='peter', password='starwars023')
        self.user.groups.add(operator_group)

    def login(self):
        self.client.force_login(self.user)

    def test_profile_update_GET_can_view(self):
        """
        Logged user can see your own profile
        """

        self.login()

        response = self.client.get(self.update_profile_url)

        self.assertEquals(response.status_code, 200)

    def test_update_profile_POST_can_update(self):
        """
        Logged user can update account infos
        """

        self.login()

        data = {
            'username': 'peterson',
            'email': 'peterson@gmail.com'
        }

        response = self.client.post(self.update_profile_url, data)

        self.user = User.objects.get(pk=self.user.pk)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.user.username, 'peterson')
        self.assertEquals(self.user.email, 'peterson@gmail.com')

    def test_update_password_POST_can_change(self):
        """
        Operator can change account password
        """

        self.login()

        data = {
            'old_password': 'starwars023',
            'new_password1': 'bigbang12313',
            'new_password2': 'bigbang12313'
        }

        response = self.client.post(self.password_change_url, data)

        self.assertRedirects(response, self.update_profile_url)
        self.assertTrue(User.objects.get(pk=self.user.pk).check_password('bigbang12313'))
