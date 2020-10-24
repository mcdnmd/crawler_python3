"""@package link_parser
Documentation for link_parser module.

Module responsible for finding href links in HTML code.
"""

from html.parser import HTMLParser
from itertools import chain


class LinkParser(HTMLParser):
    """
    HTML tags parsing
    """

    def __init__(self):
        """The constructor"""
        super().__init__()
        self.links = iter([])
        self.reset()
        self.BASE_TAGS = ['a', 'img', 'link', 'source']

    def hard_reset(self):
        """
        reset array of links for page
        """
        self.links = iter([])
        self.reset()

    def handle_starttag(self, tag, attrs):
        """
        handle chosen tag in HTML file
        @param tag: HTML tag
        @param attrs: attributes
        """
        if tag == "a":
            self.continue_cain(attrs, 'href')
        elif tag == "img" or tag == "script" or tag == "link" or tag == "source":
            self.continue_cain(attrs, "src")
        #  <source srcset="logo-480.png, logo-480-2x.png 2x">
        elif tag == "source":
            self.continue_cain(attrs, "src")

    def continue_cain(self, attrs, tag_name):
        for name, link in attrs:
            if name == tag_name:
                self.links = chain(self.links, [link])
