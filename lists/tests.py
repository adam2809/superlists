from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import homePage

class HomePageTest(TestCase):
    def testHomePageReturnsCorrectHtml(self):
        self.client.get('/')
        self.assertTemplateUsed('home.html')


    def testPOSTRequest(self):
        response = self.client.post('/', data={'reminder_name':'Buy milk','reminder_days_ahead':'1','reminder_time':'11:00'})
        responseString = response.content.decode()
        self.assertIn('Buy milk',responseString)
        self.assertIn('1',responseString)
        self.assertIn('11:00',responseString)
        self.assertTemplateUsed(response, 'home.html')
