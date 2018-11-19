from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import homePage
from lists.models import Item, List

class HomePageTest(TestCase):
    def testHomePageReturnsCorrectHtml(self):
        self.client.get('/')
        self.assertTemplateUsed('home.html')


class NewListTest(TestCase):
    def testSavesPostRequestToDB(self):
        response = self.client.post('/lists/new',data={'reminder_name':'New reminder',
        'reminder_days_ahead':'3','reminder_time':'11:00'})
        self.assertEqual(Item.objects.count(),1)
        latestReminder = Item.objects.first()
        self.assertEqual(latestReminder.name,'New reminder')
        self.assertEqual(latestReminder.daysAhead,'3')
        self.assertEqual(latestReminder.time,'11:00')


    def testRedirectsAfterPost(self):
        response = self.client.post('/lists/new',data={'reminder_name':'New reminder',
        'reminder_days_ahead':'3','reminder_time':'11:00'})
        self.assertEqual(response.status_code,302)
        self.assertRegex(response['location'],'/lists/.+')


    def testPOSTRequest(self):
        response = self.client.post('/lists/new', data={'reminder_name':'Buy milk',
        'reminder_days_ahead':'1','reminder_time':'11:00'})

        self.assertEqual(Item.objects.count(),1)

        recentItem = Item.objects.first()
        self.assertEqual(recentItem.name, 'Buy milk')
        self.assertEqual(recentItem.daysAhead, '1')
        self.assertEqual(recentItem.time, '11:00')

        response = self.client.get(f'/lists/{recentItem.list.id}/')
        responseString = response.content.decode()
        self.assertIn('Buy milk',responseString)
        self.assertIn('1',responseString)
        self.assertIn('11:00',responseString)


class DBTests(TestCase):
    def testSavingAndRetrievingReminders(self):
        lst = List()
        lst.save()

        firstItem = Item()
        firstItem.name = 'Very nice first item name'
        firstItem.daysAhead = '5'
        firstItem.time = '00:00'
        firstItem.list = lst
        firstItem.save()

        secondItem = Item()
        secondItem.name = 'Seconds item name is here'
        secondItem.daysAhead = '3'
        secondItem.time = '00:01'
        secondItem.list = lst
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(),2)

        savedList = List.objects.first()
        self.assertEquals(savedList,lst)

        firstSavedItem = savedItems[0]
        self.assertEqual(firstSavedItem.name,'Very nice first item name')
        self.assertEqual(firstSavedItem.daysAhead,'5')
        self.assertEqual(firstSavedItem.time,'00:00')
        self.assertEqual(firstSavedItem.list,lst)

        secondSavedItem = savedItems[1]
        self.assertEqual(secondSavedItem.name,'Seconds item name is here')
        self.assertEqual(secondSavedItem.daysAhead,'3')
        self.assertEqual(secondSavedItem.time,'00:01')
        self.assertEqual(secondSavedItem.list,lst)


class ListViewTest(TestCase):
    def testDisplaysAllItemsForGivenList(self):
        lst0 = List.objects.create()
        Item.objects.create(name='testname',daysAhead='3',time='00:00',list=lst0)
        Item.objects.create(name='rando name for testing',daysAhead='6',time='12:00',list=lst0)

        response = self.client.get(f'/lists/{lst0.id}/')
        self.assertContains(response,'1: testname at 00:00 in 3 days')
        self.assertContains(response,'2: rando name for testing at 12:00 in 6 days')
        self.assertNotContains(response,'1: secondname at 00:15 in 2 days')
        self.assertNotContains(response,'2: an item of list 1 at 19:03 in 10 days')

        lst1 = List.objects.create()
        Item.objects.create(name='secondname',daysAhead='2',time='00:15',list=lst1)
        Item.objects.create(name='an item of list 1',daysAhead='10',time='19:03',list=lst1)

        response = self.client.get(f'/lists/{lst1.id}/')
        self.assertContains(response,'1: secondname at 00:15 in 2 days')
        self.assertContains(response,'2: an item of list 1 at 19:03 in 10 days')
        self.assertNotContains(response,'1: testname at 00:00 in 3 days')
        self.assertNotContains(response,'2: rando name for testing at 12:00 in 6 days')


class AddViewTest(TestCase):
    def testAddsItemToExistingList(self):
        self.client.post('/lists/new',data={'reminder_name':'New reminder',
        'reminder_days_ahead':'3','reminder_time':'11:00'})

        item = Item.objects.first()
        response = self.client.get(f'/lists/{item.list.id}/')
        self.assertContains(response,'New reminder')

        self.client.post(f'/lists/add/{item.list.id}/',data={'reminder_name':'Added reminder',
        'reminder_days_ahead':'7','reminder_time':'21:00'})
        response = self.client.get(f'/lists/{item.list.id}/')
        self.assertContains(response,'Added reminder')


    def testRedirectAfterAdd(self):
        response = self.client.post('/lists/new',data={'reminder_name':'New reminder',
        'reminder_days_ahead':'3','reminder_time':'11:00'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/lists/1/')
