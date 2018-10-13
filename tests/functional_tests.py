from selenium import webdriver
import unittest

class LearningFT(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def testOpensDjngoWecomePage(self):
        self.browser.get('http://127.0.0.1:8000/')
        self.assertIn('TODO',self.browser.title)


#Checks if script was run from the command line
if __name__ == '__main__':
    unittest.main()

# LearningFT().openBrowser()
# LearningFT().testOpensDjngoWecomePage()
