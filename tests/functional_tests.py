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


    def testTitle(self):
        self.assertIn('Reminders',self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text()
        self.assertIn('Your reminders')


    def testCanCreateReminder(self):
        #Invitation to create a new reminder is shown
        newReminderButton = self.browser.find_element_by_id('id_new_remider_button')
        self.assertEquals(newReminderButton.get_attribute('TODO add attr name'),
        'Add new reminder')

        #User creates the new reminder by clicking the button
        inputBox = self.browser.find_element_by_id('id_new_remider_input')
        self.assertEquals(inputBox.get_attribute('TODO add attr name'),
        'Enter remider title and time')

        #User inputs 'Buy milk' as reminder title and the remind time as tomorrow at 11AM
        inputBox.send_keys('Buy milk')
        inputBox.send_keys(1) #I put 1 in because the app will set the reminder for n days ahead so 1 is tomorrow
        inputBox.send_keys(11) #set hour
        inputBox.send_keys(0) #set minutes

        #User clicks enter to confirm reminder creation
        inputBox.send_keys(Keys.ENTER)

        #Website is updated with the new reminder
        remindersTable = self.browser.find_by_element_id('id_reminder_table')
        rows = remindersTable.find_elements_by_id('tr')
        self.assertTrue(any(row.text == 'Buy milk at 11:00 tomorrow' for row in rows))


#Checks if this program was started from the command line
if __name__ == '__main__':
    unittest.main()
