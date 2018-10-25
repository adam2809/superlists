from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import homePage
from lists.models import Item

class HomePageTest(TestCase):
    def testHomePageReturnsCorrectHtml(self):
        self.client.get('/')
        self.assertTemplateUsed('home.html')


    def testPOSTRequest(self):
        response = self.client.post('/', data={'reminder_name':'Buy milk','reminder_days_ahead':'1','reminder_time':'11:00'})

        self.assertEqual(Item.objects.count(),1)
        self.assertEqual

        responseString = response.content.decode()
        self.assertIn('Buy milk',responseString)
        self.assertIn('1',responseString)
        self.assertIn('11:00',responseString)
        self.assertTemplateUsed(response, 'home.html')

class DBTests(TestCase):
        def testSavingAndRetrievingReminders(self):
            firstItem = Item()
            firstItem.name = 'Very nice first item name'
            firstItem.daysAhead = 5
            firstItem.time = '00:00'
            firstItem.save()

            secondItem = Item()
            secondItem.name = 'Seconds item name is here'
            secondItem.daysAhead = 3
            secondItem.time = '00:01'
            secondItem.save()

            savedItems = Item.objects.all()
            self.assertEqual(savedItems.count(),2)

            firstSavedItem = savedItems[0]
            self.assertEqual(firstSavedItem.name,'Very nice first item name')
            self.assertEqual(firstSavedItem.daysAhead,5)
            self.assertEqual(firstSavedItem.time,'00:00')

            secondSavedItem = savedItems[1]
            self.assertEqual(secondSavedItem.name,'Seconds item name is here')
            self.assertEqual(secondSavedItem.daysAhead,3)
            self.assertEqual(secondSavedItem.time,'00:01')
