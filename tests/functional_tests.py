from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        #User enters the websites URL into their browser
        self.browser.get('http://127.0.0.1:8000/')


    def tearDown(self):
        self.browser.quit()


    def testCanCreateReminder(self):
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
        self.assertEquals(inputName.get_attribute('placeholder'),
        'Name')

        inputDaysAhead = self.browser.find_element_by_id('id_new_remider_days_ahead')
        self.assertEquals(inputDaysAhead.get_attribute('placeholder'),
        'Days ahead')

        inputTime = self.browser.find_element_by_id('id_new_remider_time')
        self.assertEquals(inputTime.get_attribute('placeholder'),
        'Time')

        #User sees new reminder submit button
        submitButton = self.browser.find_element_by_tag_name('button')
        self.assertIn(submitButton.text,'Submit')

        #User inputs 'Buy milk' as reminder title and the remind time as tomorrow at 11AM
        inputName.send_keys('Buy milk')
        inputDaysAhead.send_keys(1) #I put 1 in because the app will set the reminder for n days ahead so 1 is tomorrow
        inputTime.send_keys('11:00') #set time

        #User clicks the submit button to confirm reminder creation
        submitButton.click()

        #Website is updated with the new reminder
        remindersTable = self.browser.find_element_by_id('id_reminder_table')
        rows = remindersTable.find_elements_by_id('tr')
        self.assertTrue(any(row.text == 'Buy milk at 11:00 tomorrow' for row in rows),
        'New reminder not in current reminders table')


#Checks if this program was started from the command line
if __name__ == '__main__':
    unittest.main()
