"""@package HTTPClinet
Documentation for httpclient module.

Module responsible for processing HTTP requests
"""
import os
from urllib.request import urlopen, Request
from urllib import error
from modules.Url import Url

"""
class Url:
    
    data structure
    
    def __init__(self, protocol, netloc, path):
        
        constructor
        @param protocol: HTTP or HTTPS protocol
        @param netloc: URL netloc
        @param path:  URL path

        self.scheme = protocol
        self.netloc = netloc
        self.path = path
        self.relative_path = os.path.dirname(path)
        self.basename = os.path.basename(path)
"""


class HTTPClient:
    """
    release methods for HTTP requesting
    """

    def __init__(self, timeout):
        self.timeout = timeout

    def get_content(self, url):
        """
        get content from url
        @param url: string address
        @return headers, content and page encoding
        """
        method = "GET"
        return self.make_request(url, method)

    def get_headers(self, url):
        """
        get website headers
        @param url: string address
        @return website headers
        """
        method = "HEAD"
        return self.make_request(url, method)

    def make_request(self, url, http_method):
        """
        make HTTP or HTTPS requests
        @param url: site URL address
        @param http_method: HTTP protocol type
        @return dictionary with headers, content and encoding
        """
        request = Request(url, method=http_method)
        try:
            with urlopen(request, timeout=self.timeout) as conn:
                encoding = conn.headers.get_content_charset() or 'UTF-8'
                return {"url": url,
                        "code": conn.code,
                        "type": conn.headers['Content-Type'],
                        "headers": conn.headers,
                        "content": conn.read(),
                        "encoding": encoding}
        except error.HTTPError:
            return {"url": url, "code": 500}
