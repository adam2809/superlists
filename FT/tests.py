from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

import time

import inspect

from lists.models import Item

from django.test import LiveServerTestCase

MAX_WAIT = 10\


def checkIfElementInTable(element, browser):
    remindersTable = browser.find_element_by_id('id_reminder_table')
    rows = remindersTable.find_elements_by_tag_name('tr')
    return any(row.text == element for row in rows)


def createAndWaitNewReminder(input, browser):
    #User creates another reminder
    while True:
        waitStart = time.time()
        try:
            inputName = browser.find_element_by_id('id_new_remider_name')
            inputDaysAhead = browser.find_element_by_id('id_new_remider_days_ahead')
            inputTime = browser.find_element_by_id('id_new_remider_time')
            submitButton = browser.find_element_by_tag_name('button')

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

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def testCanCreateReminderMultUsers(self):
        # First user visits the page and creates reminder
        self.browser.get(self.live_server_url)

        createAndWaitNewReminder(('Buy milk','1','11:00'),self.browser)
        self.assertTrue(checkIfElementInTable('1: Buy milk at 11:00 in 1 days',self.browser))

        currURL = self.browser.current_url
        self.assertRegex(currURL, '/lists/1')

        # First user quits
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # Second user visits page and creates reminder. They see a different table
        # than the first user
        createAndWaitNewReminder(('Go to class','4','08:55'),self.browser)

        currURL = self.browser.current_url
        self.assertRegex(currURL,'/lists/2')

        self.assertTrue(checkIfElementInTable('1: Go to class at 08:55 in 4 days',self.browser))
        self.assertFalse(checkIfElementInTable('1: Buy milk at 11:00 in 1 days',self.browser))


    def testCanCreateReminderSingleUser(self):
        #User enters the websites URL into their browser
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)


        #Test website title
        self.assertIn('Reminders',self.browser.title)

        #Test current reminders header
        currRemindersHeader = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Your reminders',currRemindersHeader.text)

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
        createAndWaitNewReminder(('Buy milk','1','11:00'),self.browser)
        self.assertTrue(checkIfElementInTable('1: Buy milk at 11:00 in 1 days',self.browser))

        #User creates second and sees it in the table
        createAndWaitNewReminder(('Go to class','4','08:55'),self.browser)
        self.assertTrue(checkIfElementInTable('2: Go to class at 08:55 in 4 days',self.browser))


class MultUsersSelectingAndAddingToList(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        self.browser.get(self.live_server_url)
    #   First user creates a reminder
        createAndWaitNewReminder(('Buy milk','1','11:00'),self)
        restartBrowser()

        # Second user visits page and creates reminder.
        createAndWaitNewReminder(('Go to class','4','08:55'),self)
        restartBrowser()


    def restartBrowser():
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()


    def testusersCanSelectListAndAddReminder():
        chooseListDropdown = self.browser.find_element_by_id('choose_list_dropdown')
        dropdownOptions = chooseListDropdown.find_elements_by_tag_name('option')

        try:
            option1 = [option for option in dropdownOptions if option.text == '1'][0]
        except IndexError:
            self.fail("List of first user not found in dropdown menu")
        option1.click()

        createAndWaitNewReminder(('something','sth','doesnt matter'),self.browser)
        assertTrue(checkIfElementInTable('2: something at sth in doesnt matter days'),self.browser)

        restartBrowser()
