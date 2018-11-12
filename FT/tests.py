from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

import time

import inspect

from lists.models import Item

from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        print('Opening browser')
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        print('Quitting browser')
        self.browser.quit()


    def checkIfElementInTable(self, element):
        remindersTable = self.browser.find_element_by_id('id_reminder_table')
        rows = remindersTable.find_elements_by_tag_name('tr')
        caller = inspect.getouterframes(inspect.currentframe(),2)[1][3]
        print(f'Current table text:\n{remindersTable.text}\nCalled by {caller}')
        return any(row.text == element for row in rows)


    def createAndWaitNewReminder(self, input):
        #User creates another reminder
        while True:
            waitStart = time.time()
            try:
                inputName = self.browser.find_element_by_id('id_new_remider_name')
                inputDaysAhead = self.browser.find_element_by_id('id_new_remider_days_ahead')
                inputTime = self.browser.find_element_by_id('id_new_remider_time')
                submitButton = self.browser.find_element_by_tag_name('button')

                inputName.send_keys(input[0])
                inputDaysAhead.send_keys(input[1])
                inputTime.send_keys(input[2])

                #User clicks the submit button to confirm reminder creation
                submitButton.click()
            except StaleElementReferenceException as e:
                if time.time() - waitStart > MAX_WAIT:
                    raise e
                print('Waiting for elements to load...')
                time.sleep(0.2)
                continue
            break


    def testCanCreateReminderMultUsers(self):
        # First user visits the page and creates reminder
        self.browser.get(self.live_server_url)

        self.createAndWaitNewReminder(('Buy milk','1','11:00'))
        self.assertTrue(self.checkIfElementInTable('1: Buy milk at 11:00 in 1 days'))

        currURL = self.browser.current_url
        self.assertRegex(currURL, '/lists/.+')

        # First user quits
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Second user visits page and creates reminder. They see a different table
        # than the first user
        self.createAndWaitNewReminder(('Go to class','4','08:55'))

        currURL = self.browser.current_url
        self.assertRegex('/lists/.+')

        self.assertTrue(self.checkIfElementInTable('1: Go to class at 08:55 in 4 days'))
        self.assertFalse(self.checkIfElementInTable('1: Buy milk at 11:00 in 1 days'))


    def testCanCreateReminderSingleUser(self):

        reminderTextList = [f'{r.id}: {r.name} at {r.time} in {r.daysAhead} days'
                        for r in Item.objects.all()]
        print(f"Reminders in database: {reminderTextList}")
        #User enters the websites URL into their browser
        self.browser.get(self.live_server_url)

        #Test website title
        self.assertIn('Reminders',self.browser.title)

        #Test current reminders header
        currRemindersHeader = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your reminders',currRemindersHeader)

        #User sees new reminder header
        newReminderHeader = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('New reminder', newReminderHeader)

        #User sees the new reminder inputs: name, days ahead, hour and minutes
        inputName = self.browser.find_element_by_id('id_new_remider_name')
        self.assertEqual(inputName.get_attribute('placeholder'),
        'Name')

        inputDaysAhead = self.browser.find_element_by_id('id_new_remider_days_ahead')
        self.assertEqual(inputDaysAhead.get_attribute('placeholder'),
        'Days ahead')

        inputTime = self.browser.find_element_by_id('id_new_remider_time')
        self.assertEqual(inputTime.get_attribute('placeholder'),
        'Time')

        #User sees new reminder submit button
        submitButton = self.browser.find_element_by_tag_name('button')
        self.assertIn(submitButton.text,'Submit')

        #User creates new reminder and sees it in the table
        self.createAndWaitNewReminder(('Buy milk','1','11:00'))
        self.assertTrue(self.checkIfElementInTable('1: Buy milk at 11:00 in 1 days'))

        #User creates second and sees it in the table
        self.createAndWaitNewReminder(('Go to class','4','08:55'))
        self.assertTrue(self.checkIfElementInTable('2: Go to class at 08:55 in 4 days'))