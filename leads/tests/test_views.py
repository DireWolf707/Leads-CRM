from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse("home"))

    def test_status_code(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template_name(self):
        self.assertTemplateUsed(self.resp, 'home.html')
