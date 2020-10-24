import os
import re
from urllib.parse import urlparse


class UrlParserUtils:
    def __init__(self):
        self.ASSET_PATTERN = re.compile(
            r'([.|\w|\s|-])*\.(?:jpg|jpeg|gif|png)',
            re.IGNORECASE
        )

    def get_asset_filename(self, url):
        return self.ASSET_PATTERN.fullmatch(url).group()


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
        name = os.path.basename(self.path)
        if name == '':
            name += 'index.html'
        return name
