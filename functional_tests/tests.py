from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time> MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
        self.wait_for_row_in_list_table('1: Contact Charitable Organisations')

        #There is still a text box inviting her to add another item.
        #He enters 'build app'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('build app')
        inputbox.send_keys(Keys.ENTER)


        #The page updates again, now showing both his items in the list
        self.wait_for_row_in_list_table('1: Contact Charitable Organisations')
        self.wait_for_row_in_list_table('2: build app')

        #He wonders whether the site will remember his list. He sees that
        #the site has generated a unique URL for her
        #self.fail('Finish the test!')

        #she visits that url, and finds her to-do list is still there

        #Satisfied, Jack goes back to sleep
        #browser.quit()
    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Jack starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #He notices that her list has  a unique url
        jack_list_url = self.browser.current_url
        self.assertRegex(jack_list_url, '/lists/.+')

        #Now a new user, Tim, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Jack's is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Tim visits the home page. There is no sign of Jack's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Tim starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Tim gets his own unique URL
        tim_list_url = self.browser.current_url
        self.assertRegex(tim_list_url, '/lists/.+')
        self.assertNotEqual(tim_list_url, jack_list_url)

        #Again, there is no trace of Jack's List
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #satisfied, they both go back to sleep

    def test_layout_and_styling(self):
        #jack goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] +inputbox.size['width'] /2,
            512,
            delta=10
        )

        #He starts a new list and sees the input is nicely centered
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 10
        )