from html.parser import HTMLParser
from itertools import chain


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = iter([])
        self.reset()

    def hard_reset(self):
        self.links = iter([])
        self.reset()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, link in attrs:
                if name == "href":
                    self.links = chain(self.links, [link])
