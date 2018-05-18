from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jack heard about this new cool online to-do app
        # he goes check the homepage
        self.browser.get(self.live_server_url)

        #he then notices the page title and header mention to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        #He types "Contact Charitable Organisations" into a
        #txt box
        inputbox.send_keys('Contact Charitable Organisations')


        #WHen he his enter, the page updates and the page list
        #'1: Contact Charitable Organisation" as an item in the to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Contact Charitable Organisations')

        #There is still a text box inviting her to add another item.
        #He enters 'build app'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('build app')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        #The page updates again, now showing both his items in the list
        self.check_for_row_in_list_table('1: Contact Charitable Organisations')
        self.check_for_row_in_list_table('2: build app')

        #He wonders whether the site will remember his list. He sees that
        #the site has generated a unique URL for her
        self.fail('Finish the test!')

    #she visits that url, and finds her to-do list is still there

    #Satisfied, Jack goes back to sleep
    #browser.quit()