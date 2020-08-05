
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import Group, User 

from apps.accounts.views import users_list, login_page, register_page

class AccountViewTest(TestCase):
  
  def setUp(self):
    self.client = Client() 
    self.factory = RequestFactory()

    adminGroup = Group.objects.create(name='Admin')
    operatorGroup = Group.objects.create(name='Operator')

    self.user1 = User.objects.create_user(username='admin', password='farcryw023')
    self.user2 = User.objects.create_user(username='jonhdoe', password='farcryw023')

    self.user1.groups.add(adminGroup)
    self.user2.groups.add(operatorGroup)


  def test_users_list_GET_can_view(self):
    """
    A logged user that belongs to admin group 
    can access /list-users page
    """
    request = self.factory.get('/users-list/')
    request.user = self.user1

    response = users_list(request)

    self.assertEquals(response.status_code, 200)


  def test_users_list_GET_restricted(self):
    """
    users list page is restricted to users 
    that belongs to operator grouè
    """
    request = self.factory.get('/users-list/')
    request.user = self.user2

    response = users_list(request)

    self.assertEquals(response.status_code, 302)


  def test_users_list_GET_redirected(self):
    """
    Unlogged users cannot access list_users url
    instead, they get redirected to the login page
    """
    response = self.client.get(reverse('list_users'))

    self.assertRedirects(response, '/login/?next=/users-list/')

  
  def test_dashboard_GET_redirected(self):
    """
    Unlogged users cannot access dashboard page
    instead, they get redirected to the login page
    """
    response = self.client.get(reverse('dashboard'))

    self.assertRedirects(response, '/login/?next=/')


  def test_login_GET_restricted(self):
    """
    Logged users cannot access login page
    """
    request = self.factory.get('/login/')
    request.user = self.user1

    response = login_page(request)

    self.assertEquals(response.status_code, 302)

  
  def test_register_POST_can_create_user(self):
    """
    Logged users cannot access login page
    """
    data = {
      'username': 'peter',
      'password': '123456',
      'group': 1
    }

    request = self.factory.post('/register/', data)
    request.user = self.user1

    response = register_page(request)

    self.assertEquals(response.status_code, 302)
