import unittest
import unittest.mock as mock
from modules.Crawler import Crawler
from modules.SafeStates import StateHandler

URL = 'https://test.org'
FOLDER = '/home/root/test.org'
FILTERS = [['css'], ['js'], ['xml']]


class CrawlerTest(unittest.TestCase):
    def setUp(self):
        state_handler = StateHandler(FOLDER)
        self.crawler = Crawler(URL, FOLDER, 3, 4, FILTERS, state_handler)

    def test_process_data_response(self):
        pass

    def test_process_html_content(self):
        pass

    def test_process_filter_content(self):
        pass

    def test_create_url(self):
        url = self.crawler.create_url('robots.txt')
        self.assertEqual(url, URL + '/robots.txt')

    def test_define_content_type(self):
        pass

    def test_is_url_disallow(self):
        class NewRobotsHandler(object):
            def __init__(self):
                self.allow_links = ['https://test.org/pics/hello_hacker.png',
                                    'https://test.org/api/request/quote/']
                self.disallow_links = {'https://test.org/pics',
                                       'https://test.org/api'}

        self.crawler.RobotsHandler = NewRobotsHandler()
        url = 'https://https://test.org/pics/hello_bro.jpeg'
        self.assertFalse(self.crawler.is_url_disallow(url))

    def test_check_asset_size(self):
        pass
