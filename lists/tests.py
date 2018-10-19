from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import homePage

class HomePageTest(TestCase):
    def testHomePageReturnsCorrectHtml(self):
        self.client.get('/')

        self.assertTemplateUsed('home.html')
