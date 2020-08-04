from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User 

from .models import Employer

class AccountViewTest(TestCase):
  
  def setUp(self):
    self.client = Client() 

  
  def test_users_list_GET(self):
    response = self.client.get(reverse('list_users'))

    self.assertEquals(response.status_code, 200)
    