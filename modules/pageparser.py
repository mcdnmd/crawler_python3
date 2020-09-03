"""@package pageparser
Documentation for linkparser module.

Module responsible for verifying href links.
"""


from urllib.parse import urlparse, urljoin
from modules.linkparser import LinkParser


class PageParser:
    """
    page parsing and URL verifying
    """

    def __init__(self, scheme, netloc, image_filter, visited):
        """ The constructor
        @param scheme: URL scheme
        @param netloc: URL netloc
        @param image_filter: prohibited file extensions
        @param visited: set of visited links
        """
        self.LinkParser = LinkParser()
        self.scheme = scheme
        self.netloc = netloc
        self.base_url = scheme + '://' + netloc
        self.path = None
        self.image_suffixes = image_filter
        self.visited_pages = visited

    def gen_links(self, html):
        """
        find links in HTML code
        @param html: HTML file
        @return link
        """
        for line in html:
            self.LinkParser.feed(line)
            yield from self.LinkParser.links

    def link_domain_is_allowed(self, url):
        """
        check is address allowed
        @param url URL of file
        @return boolean
        """
        parsed = urlparse(url)
        return parsed.scheme == self.scheme and parsed.netloc == self.netloc

    def is_image(self, url):
        """
        check is address point to image
        @param url: URL of file
        @return boolean
        """
        for suffix in self.image_suffixes:
            if url.endswith(suffix):
                return True
        return False

    def get_filtered_links(self, html):
        """
        get links from HTML code
        @param html: HTML file
        @return list of links or None
        """
        result = []
        norm_links = self.normalize_links(self.gen_links(html))
        for link in norm_links:
            if self.link_domain_is_allowed(link) \
                    and link not in self.visited_pages \
                    and not self.is_image(link):
                result.append(link)
                self.visited_pages.add(link)
        return result or None

    def normalize_links(self, links):
        """
        normalize links and remove useless URL data
        @param links: list of URL links
        @return list of normalized links
        """
        return [self.normalize_link(link) for link in links]

    def normalize_link(self, link):
        """
        remove useless URL data
        @param link: URL link
        @return string normalized link
        """
        base = self.base_url
        return self.remove_extra(urljoin(base, link))

    def remove_extra(self, url):
        """
        remove extra data on the end of URL link
        @param url: URL link
        @return string URL without URL metadata
        """
        parsed = urlparse(url)
        self.path = parsed.path
        return parsed.scheme + '://' + parsed.netloc + parsed.path
