"""@package page_parser
Documentation for page_parser module.

Module responsible for verifying href links.
"""


from urllib.parse import urlparse, urljoin
from modules.LinkParser import LinkParser


class PageParser:
    """
    page parsing and URL verifying
    """

    def __init__(self, url, visited):
        """
        The constructor
        @param url: Url class
        @param visited: set of visited links
        """
        self.LinkParser = LinkParser()
        self.general_url = url
        self.path = None
        self.visited_pages = visited

    def gen_links(self, html):
        """
        find links in HTML code
        @param html: HTML file
        @return link
        """
        for line in html.split('\n'):
            self.LinkParser.feed(line)
            yield from self.LinkParser.links

    def link_domain_is_allowed(self, url):
        """
        check is address allowed
        @param url URL of file
        @return boolean
        """
        parsed = urlparse(url)
        return parsed.scheme == self.general_url.scheme and \
               parsed.netloc == self.general_url.netloc or url.startswith('/')

    def get_filtered_links(self, html):
        """
        get links from HTML code
        @param html: HTML file
        @return list of classes Urls or None
        """
        result = []
        links = self.gen_links(html)
        for link in links:
            url = urljoin(self.general_url.baseurl, link)
            if self.link_domain_is_allowed(url):
                result.append(url)
        return result or None
