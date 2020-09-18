"""@package test_page
Documentation for test_page module.

Module responsible for testing util modules.
"""
import os
import unittest
from urllib.parse import urlparse
from modules.page_parser import PageParser
from modules.crawler import Crawler
from modules.robots_parser import RobotsParser
from modules.safe_states import StateHandler

LINK = "site_forUnitTests/new/folder/"
SIMPLE_FILTER = ['.png', '.jpg', 'jpeg', '.gif']
ROOT_LINK = "https://www.test.com/"
TEST_PAGE = PageParser("https", "www.test.com", SIMPLE_FILTER, set())
PATH = os.path.abspath('test_page.py' + '/..') + "/"


class PageTest(unittest.TestCase):
    """
    unit tests
    """
    def test_remove_extra(self):
        link = ROOT_LINK + "index.html#x-headers"
        TEST_PAGE.LinkParser.hard_reset()
        result = TEST_PAGE.remove_extra(link)
        self.assertEqual(ROOT_LINK + 'index.html', result)

    def test_normalize_links(self):
        links = [ROOT_LINK + "getRecords?apikey=$api_key&ticket=$ticket_id",
                 ROOT_LINK + "shop.html",
                 ROOT_LINK + "a_good_link",
                 ROOT_LINK + "index?=.html?=query_in_data_base"]
        NORMALIZE = ['https://www.test.com/getRecords',
                     'https://www.test.com/shop.html',
                     'https://www.test.com/a_good_link',
                     'https://www.test.com/index']
        TEST_PAGE.LinkParser.hard_reset()
        result = TEST_PAGE.normalize_links(links)
        self.assertEqual(NORMALIZE, result)

    def test_domain_is_allowed(self):
        link = ROOT_LINK + "i_am_a_good_url"
        TEST_PAGE.LinkParser.hard_reset()
        self.assertEqual(True, TEST_PAGE.link_domain_is_allowed(link))

    def test_domain_is_not_allowed(self):
        link = "http://www.test.com/i_am_a_bad_url"
        TEST_PAGE.LinkParser.hard_reset()
        self.assertEqual(False, TEST_PAGE.link_domain_is_allowed(link))

    def test_extract_links_from_html(self):
        count = 0
        TEST_PAGE.LinkParser.hard_reset()
        with open(PATH + "extract_links_test.html", 'r') as html:
            for _ in TEST_PAGE.gen_links(html):
                count += 1
        self.assertEqual(7, count)

    def test_get_filtred_links(self):
        links = ["https://www.test.com/", "https://www.test.com/new_page"]
        TEST_PAGE.LinkParser.hard_reset()
        with open(PATH + "get_links_test_1.html", 'r') as html:
            result = TEST_PAGE.get_filtered_links(html)
        self.assertEqual(links, result)

    def test_image_filter(self):
        links = set()
        links.add("https://www.test.com/")
        links.add("https://www.test.com/new_image_info.txt")
        links.add("https://www.test.com/new_page")
        TEST_PAGE.LinkParser.hard_reset()
        with open(PATH + "image_filter_test.html", 'r') as html:
            result = TEST_PAGE.get_filtered_links(html)
        self.assertTrue(self.is_result_in_set(links, result))

    def test_robots_webrules(self):
        link = "https://ru.wikipedia.org/robots.txt"
        url = urlparse(link)
        s = StateHandler()
        c = Crawler(url,LINK,1,512,SIMPLE_FILTER, s)
        r = RobotsParser()
        result = r.get_strict_rules(c.make_robots_request())
        self.assertTrue(len(result) == 249)


    def is_result_in_set(self, links, result):
        count = 0
        result_len = len(result)
        for link in result:
            if link in links:
                count += 1
        return result_len == count


