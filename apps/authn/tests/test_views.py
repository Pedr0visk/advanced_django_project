from django.test import TestCase, Client, RequestFactory

class AuthViewTest(TestCase):
  def test_login_GET_restricted(self):
    """
    Logged users cannot access login page
    """
    request = self.factory.get('/login/')
    request.user = self.user1

    response = login_page(request)

    self.assertEquals(response.status_code, 302)