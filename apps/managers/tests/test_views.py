
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import Group, User, Permission 
from django.contrib.contenttypes.models import ContentType

from apps.managers.views import accounts_list, login_page, register_page

class AccountViewTest(TestCase):
  
  def setUp(self):
    self.client = Client() 
    self.factory = RequestFactory()

    # for the tests puporse will be needed 3 types of groups
    adminGroup = Group.objects.create(name='Admin')
    guestGroup = Group.objects.create(name='Guest')
    operatorGroup = Group.objects.create(name='Operator')

    content_type = ContentType.objects.get_for_model(User)
    user_permissions = Permission.objects.filter(content_type=content_type)

    # add all the permissions of user to adminGroup
    for p in user_permissions:
      adminGroup.permissions.add(p)

    # add just view_account permission to guestGroup
    guestGroup.permissions.add(user_permissions[0])

    """
      Create 3 users to test in this order: Admin > Operator > Guest.
      All the tests are based on this 3 users, take care when refactoring this tests, 
      changing the number of users create for this tests can cause errors.
    """
    self.user1 = User.objects.create_user(username='admin', password='farcryw023')
    self.user2 = User.objects.create_user(username='jonhdoe', password='farcryw023')
    self.user3 = User.objects.create_user(username='luccas', password='farcryw023')

    # assign groups to the users
    self.user1.groups.add(adminGroup)
    self.user2.groups.add(operatorGroup)
    self.user3.groups.add(guestGroup)


  def test_accounts_list_GET_can_view(self):
    """
    A logged user that belongs to admin group 
    can access /manager/accounts page
    """
    request = self.factory.get('/users-list/')
    request.user = self.user1

    response = accounts_list(request)

    self.assertEquals(response.status_code, 200)


  def test_accounts_list_GET_restricted(self):
    """
    operator users cannot access accounts list page
    """
    self.client.force_login(self.user2)

    response = self.client.get('/manager/register/')

    self.assertEquals(response.status_code, 302)


  def test_accounts_list_GET_redirected(self):
    """
    Unlogged users cannot access list_accounts url
    instead, they get redirected to the login page
    """
    response = self.client.get(reverse('list_accounts'))

    self.assertRedirects(response, '/login/?next=/manager/accounts/')

  
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

    response = self.client.post('/manager/register/', {
      'username': 'peter',
      'email': 'peter@example.com',
      'password1': 'pass0rdkms',
      'password2': 'pass0rdkms',
      'group': 'Admin'
    })


    self.assertEquals(User.objects.count(), 4)
    self.assertEquals(User.objects.get(username='peter').email, 'peter@example.com')
    self.assertEquals(response.status_code, 302)


  def test_register_POST_cannot_create_admin_account(self):
    """
    An operator user cannot register an account
    """
    self.client.force_login(self.user2)

    response = self.client.post('/manager/register/', {
      'username': 'peter',
      'email': 'peter@example.com',
      'password1': 'pass0rdkms',
      'password2': 'pass0rdkms',
      'group': 'Admin'
    })

    self.assertEquals(User.objects.count(), 3)
    self.assertEquals(response.status_code, 302)
