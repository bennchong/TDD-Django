from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jack heard about this new cool online to-do app
        # he goes check the homepage
        self.browser.get('http://localhost:8000')

        #he then notices the page title and header mention to-do list
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

    #He is invited to enter a to-do item straight away

    #He types "Contact Charitable Organisations" into a
    #txt box

    #WHen he his enter, the page updates and the page list
    #'1: Contact Charitable Organisation" as an item in the to-do list

    #There is still a text box inviting her to add another item.
    #He enters 'build app'

    #The page updates again, now showing both his items in the list

    #He wonders whether the site will remember his list. He sees that
    #the site has generated a unique URL for her

    #she visits that url, and finds her to-do list is still there

    #Satisfied, Jack goes back to sleep
    #browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')