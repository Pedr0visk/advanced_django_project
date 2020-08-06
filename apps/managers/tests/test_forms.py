from django.test import SimpleTestCase
from apps.accounts.forms import CreateUserForm

class TestForms(SimpleTestCase):
  
  def text_user_form_valid_data(self):
    form = CreateUserForm(data={
      'username': 'peter',
      'password1': 'passw0rd123',
      'password2': 'passw0rd123',
      'email': 'peter@example.com',
    })

    print('here')
    self.assertTrue(form.is_valid())

  
  def test_user_form_no_data(self):
    form = CreateUserForm(data={})
    
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 3)