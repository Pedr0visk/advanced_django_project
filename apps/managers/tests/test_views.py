from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType

from apps.managers.forms import UserForm


class AccountViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # default urls
        self.accounts_list_url = reverse('list_accounts')
        self.register_account_url = reverse('register_account')
        self.manager_dash_url = reverse('manager')

        # for the tests puporse will be needed 3 types of groups
        admin_group = Group.objects.create(name='Admin')
        guest_group = Group.objects.create(name='Guest')
        operator_group = Group.objects.create(name='Operator')

        content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(content_type=content_type)

        # add all the permissions of user to adminGroup
        for p in user_permissions:
            admin_group.permissions.add(p)

        # add just view_account permission to guestGroup
        guest_group.permissions.add(user_permissions[0])

        """
        Create 3 users to test in this order: Admin > Operator > Guest.
        All the tests are based on this 3 users, take care when refactoring this tests, 
        changing the number of users create for this tests can cause errors.
        """
        self.user1 = User.objects.create_user(username='admin', password='farcryw023')
        self.user2 = User.objects.create_user(username='jonhdoe', password='farcryw023')
        self.user3 = User.objects.create_user(username='luccas', password='farcryw023')

        # assign groups to the users
        self.user1.groups.add(admin_group)
        self.user2.groups.add(operator_group)
        self.user3.groups.add(guest_group)

    def test_list_accounts_GET_can_view(self):
        """
    A logged user that belongs to admin group 
    can access /manager/accounts page
    """
        self.client.force_login(self.user1)

        response = self.client.get(self.accounts_list_url)

        self.assertEquals(response.status_code, 200)

    def test_list_accounts_GET_restricted(self):
        """
    operator users cannot access accounts list page
    """
        self.client.force_login(self.user2)

        response = self.client.get(reverse('register_account'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             '/manager/unauthorized/?next=/manager/register_account/',
                             status_code=302,
                             target_status_code=200)

    def test_list_accounts_GET_redirected(self):
        """
    Not logged users cannot access list_accounts url
    instead, they get redirected to the login page
    """
        response = self.client.get(self.accounts_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             '/manager/login/?next=/manager/list_accounts/',
                             status_code=302,
                             target_status_code=200)

    def test_dashboard_GET_redirected(self):
        """
    Unlogged users cannot access dashboard page
    instead, they get redirected to the login page
    """
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(response, '/login/?next=/')

    def test_register_POST_can_create_admin_account(self):
        """
        Admin user can create another admin user
        """
        self.client.force_login(self.user1)

        response = self.client.post(self.register_account_url, self.user_data())

        self.assertEquals(User.objects.count(), 4)
        self.assertEquals(User.objects.get(username='peter').email, 'peter@example.com')
        self.assertEquals(response.status_code, 302)

    def test_register_POST_cannot_create_admin_account(self):
        """
    An operator user cannot register an account
    """
        self.client.force_login(self.user2)

        response = self.client.post('/manager/register_account/', {
            'username': 'peter',
            'email': 'peter@example.com',
            'password1': 'pass0rdkms',
            'password2': 'pass0rdkms',
            'group': 'Admin'
        })

        self.assertEquals(User.objects.count(), 3)
        self.assertEquals(response.status_code, 302)

    def test_manager_GET_guest_has_no_access(self):
        """
    A guest user cannot have access to the manager area
    """

        self.client.force_login(self.user3)

        response = self.client.get(self.manager_dash_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             '/manager/unauthorized/?next=/manager/',
                             status_code=302,
                             target_status_code=200)

    def test_update_account_GET_can_be_returned(self):

        self.client.force_login(self.user1)

        response = self.client.get('/manager/update_account/%s/' % self.user2.pk)

        self.assertEquals(response.status_code, 200)

    def test_update_account_GET_404_user_not_found(self):
        self.client.force_login(self.user1)

        response = self.client.get('/manager/update_account/%s/' % 13123)

        self.assertEquals(response.status_code, 404)

    def test_update_account_POST_can_be_updated(self):
        """
        An account can be updated by manager
        """

        self.client.force_login(self.user1)

        response = self.client.post('/manager/update_account/%s/' % self.user2.pk, {
          'username': 'pedro',
          'email': 'pedro357bm@gmail.com',
          'group': 'Admin'
        })

        updated_user2 = User.objects.get(pk=self.user2.pk)

        self.assertRedirects(response, self.accounts_list_url)
        self.assertEquals(updated_user2.username, 'pedro')
        self.assertEquals(updated_user2.email, 'pedro357bm@gmail.com')
        self.assertEquals(updated_user2.groups.all()[0].name, 'Admin')

    def test_delete_account_GET_show_confirm_form(self):
        """
        A confirm form is shown to delete an account
        """

        self.client.force_login(self.user1)

        response = self.client.get('/manager/delete_account/%s/' % self.user2.pk)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'managers/account_confirm_delete.html')

    def test_delete_account_POST_can_delete(self):
        """
        An account can be deleted by manager
        """

        self.client.force_login(self.user1)

        response = self.client.post('/manager/delete_account/%s/' % self.user2.pk)

        self.assertRedirects(response, self.accounts_list_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 2)

    @staticmethod
    def user_data():
        """
        Private function that returns data for user creation
        """
        return {
            'username': 'peter',
            'email': 'peter@example.com',
            'password1': 'pass0rdkms',
            'password2': 'pass0rdkms',
            'group': 'Admin'
        }
