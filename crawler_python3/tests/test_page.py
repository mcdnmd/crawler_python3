import unittest
from modules.pageparser import PageParser

LINK = "site_forUnitTests/new/folder/"
SIMPLE_FILTER = ['.png', '.jpg', 'jpeg', '.gif']
TLINK = "https://www.test.com/"
TEST_PAGE = PageParser("https", "www.test.com", SIMPLE_FILTER)


class PageTest(unittest.TestCase):
    def test_remove_extra(self):
        LINK = TLINK + "index.html#x-headers"
        TEST_PAGE.LinkParser.hard_reset()
        result = TEST_PAGE.remove_extra(LINK)
        self.assertEqual(TLINK + 'index.html', result)

    def test_normalize_links(self):
        LINKS = [TLINK + "getRecords?apikey=$api_key&ticket=$ticket_id",
                 TLINK + "shop.html",
                 TLINK + "a_good_link",
                 TLINK + "index?=.html?=query_in_data_base"]
        NORMALIZE = ['https://www.test.com/getRecords',
                     'https://www.test.com/shop.html',
                     'https://www.test.com/a_good_link',
                     'https://www.test.com/index']
        TEST_PAGE.LinkParser.hard_reset()
        result = TEST_PAGE.normalize_links(LINKS)
        self.assertEqual(NORMALIZE, result)

    def test_domain_is_allowed(self):
        LINK = TLINK + "i_am_a_good_url"
        TEST_PAGE.LinkParser.hard_reset()
        self.assertEqual(True, TEST_PAGE.link_domain_is_allowed(LINK))

    def test_domain_is_not_allowed(self):
        LINK = "http://www.test.com/i_am_a_bad_url"
        TEST_PAGE.LinkParser.hard_reset()
        self.assertEqual(False, TEST_PAGE.link_domain_is_allowed(LINK))

    def test_extract_links_from_html(self):
        count = 0
        TEST_PAGE.LinkParser.hard_reset()
        with open("extract_links_test.html", 'r') as html:
            for _ in TEST_PAGE.gen_links(html):
                count += 1
        self.assertEqual(7, count)

    def test_get_filtred_links(self):
        LINKS = ["https://www.test.com/", "https://www.test.com/new_page"]
        TEST_PAGE.LinkParser.hard_reset()
        with open("get_links_test_1.html", 'r') as html:
            result = TEST_PAGE.get_filtred_links(html)
        self.assertEqual(LINKS, result)

    def test_image_filter(self):
        LINKS = set()
        LINKS.add("https://www.test.com/")
        LINKS.add("https://www.test.com/new_image_info.txt")
        LINKS.add("https://www.test.com/new_page")
        TEST_PAGE.LinkParser.hard_reset()
        with open("image_filter_test.html", 'r') as html:
            result = TEST_PAGE.get_filtred_links(html)
        self.assertTrue(self.is_result_in_set(LINKS, result))
        #self.assertEqual(LINKS, result)

    def is_result_in_set(self, links, result):
        count = 0
        l = len(result)
        for link in result:
            if link in links:
                count += 1
        return l == count