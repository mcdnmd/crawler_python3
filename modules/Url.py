import os
from urllib.parse import urlparse


class Url:
    def __init__(self, url):
        self.URL = url
        parsed = urlparse(url)
        self.scheme = parsed.scheme
        self.netloc = parsed.netloc
        self.path = parsed.path
        self.baseurl = self.scheme + '://' + self.netloc
        self.filename = self.get_file_name()
        self.dirname = os.path.dirname(self.path)
        self.abspath = os.path.join(self.dirname, self.filename)

    def get_file_name(self):
        return os.path.basename(self.path) or 'index.html'
