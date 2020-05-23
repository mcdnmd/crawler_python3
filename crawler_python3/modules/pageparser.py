import re
from urllib.parse import urlparse, urljoin
from modules.linkparser import LinkParser


class PageParser:
    def __init__(self, scheme, netloc, image_filter):
        self.LinkParser = LinkParser()
        self.scheme = scheme
        self.netloc = netloc
        self.base_url = scheme + '://' + netloc
        self.path = None
        self.image_suffixes = image_filter
        self.visited_pages = set()

    def gen_links(self, html):
        for line in html:
            self.LinkParser.feed(line)
            yield from self.LinkParser.links

    def link_domain_is_allowed(self, url):
        parsed = urlparse(url)
        return parsed.scheme == self.scheme and parsed.netloc == self.netloc

    def is_image(self, url):
        for suffix in self.image_suffixes:
            if url.endswith(suffix):
                return True
        return False

    def get_filtred_links(self, html):
        result = []
        norm_links = self.normalize_links(self.gen_links(html))
        for link in norm_links:
            if self.link_domain_is_allowed(link) \
                    and link not in self.visited_pages \
                    and not self.is_image(link):
                result.append(link)
                self.visited_pages.add(link)
        if len(result) != 0:
            return result
        else:
            return None

    def normalize_links(self, links):
        return [self.normalize_link(link) for link in links]

    def normalize_link(self, link):
        base = self.base_url
        return self.remove_extra(urljoin(base, link))

    def remove_extra(self, url):
        parsed = urlparse(url)
        self.path = parsed.path
        return parsed.scheme + '://' + parsed.netloc + parsed.path

