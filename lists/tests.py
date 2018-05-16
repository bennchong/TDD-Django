from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.
class homePageTest(TestCase):

    def test_root_resolves(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

