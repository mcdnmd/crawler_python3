import re
from urllib.parse import urlparse
import startup


class Page:
    def __init__(self, link, depth=5):
        self.MAX_DEPTH = startup.MAX_DEPTH
        self.VISITED = startup.VISITED
        self.link = link
        self.depth = depth
        self.response = None
        self.filename = None
        self.norm_link = None
        self.possible_pages = []

    def load_content(self, response):
        self.response = response

    def extract_links(self):
        if self.depth >= self.MAX_DEPTH:
            return None
        pattern = r'<a\s.*?href=\"http.+://(.+?)\".*?>.+?</a>'
        regex = re.compile(pattern, re.IGNORECASE)
        mo = regex.findall(self.response.text)
        for re_link in mo:
            if re_link.find(self.link) != -1:
                re_link = self.link + '/' + urlparse(re_link).path
                if re_link is not None and re_link not in self.VISITED:
                    self.VISITED.add(re_link)
                    self.possible_pages.append(Page(re_link, self.depth + 1))

    def create_filename(self):
        pattern = r'http.?://([\w./_-]*[^/])'
        compiled = re.compile(pattern)
        self.filename = (compiled.findall(self.response.url)[0] + '.html')\
            .replace('/', '.')
