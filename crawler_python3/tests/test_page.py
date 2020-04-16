import unittest
import pytest
from modules import page

LINK = "site_forUnitTests/new/folder/"


class PageTest(unittest.TestCase):
    def test_initialization_link(self):
        t_page = page.Page(LINK, 0)
        self.assertEqual(LINK, t_page.link)

    def test_initialization_depth(self):
        t_page = page.Page(LINK, 4)
        self.assertEqual(4, t_page.depth)

    def test_get_possible_pages(self):
        t_page = page.Page(LINK, 6)
        self.assertEqual(None, t_page.extract_links())
