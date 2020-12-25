"""@package test_page
Documentation for test_page module.

Module responsible for testing util modules.
"""
import os
import unittest
from urllib.parse import urljoin

from modules.PageParser import PageParser
from modules.TerminalParser import TerminalParser
from modules.Url import Url

ROOT_LINK = "https://www.test.com"
pageparser = PageParser(Url("https://www.test.com"), set())
PATH = os.path.dirname(__file__)


class PageTest(unittest.TestCase):
    """
    unit tests
    """
    def test_terminal_parser_weburl(self):
        t = TerminalParser()
        urls = ['htt://test.org',
                'test.org',
                'https:/test.org',
                'htt://test.org']
        for i in urls:
            with self.subTest(i=i):
                self.assertRaises(ValueError, lambda: t.verify_wed_url(i))

    def test_domain_is_allowed(self):
        link = urljoin(ROOT_LINK, "i_am_a_good_url")
        pageparser.LinkParser.hard_reset()
        self.assertEqual(True, pageparser.link_domain_is_allowed(link))

    def test_domain_is_not_allowed(self):
        link = "http://www.test.com/i_am_a_bad_url"
        pageparser.LinkParser.hard_reset()
        self.assertEqual(False, pageparser.link_domain_is_allowed(link))

    def test_extract_links_from_html(self):
        count = 0
        pageparser.LinkParser.hard_reset()
        filename = os.path.join(PATH, "test_samples/extract_links_test.html")
        with open(filename, 'r') as html:
            for _ in pageparser.gen_links(html.read()):
                count += 1
        self.assertEqual(7, count)

    def test_get_filtred_links(self):
        links = ["https://www.test.com/", "https://www.test.com/new_page"]
        pageparser.LinkParser.hard_reset()
        filename = os.path.join(PATH, "test_samples/get_links_test_1.html")
        with open(filename, 'r') as html:
            result = pageparser.get_filtered_links(html.read())
        self.assertEqual(links, result)
