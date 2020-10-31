"""@package robots_parser
Documentation for robots_parser module.

Module responsible for defining crawling rules
"""
from urllib.parse import urljoin

from modules.Url import Url


class RobotsHandler:
    """
    parser robots.txt files
    """

    def __init__(self, url):
        self.general_url = Url(url)
        self.user_agent = 'User-agent: *'
        self.disallow_syntax = 'Disallow'
        self.allow_syntax = 'Allow'
        self.allow_links = []
        self.disallow_links = []
        self.parse_rules_flag = False
        self.HTTP_CLIENT = None

    def initialize(self, http_client):
        self.HTTP_CLIENT = http_client

    def get_rules(self, url):
        """
        get rules Disallow from server
        @param url: robots.txt file content
        """
        resp_code = self.HTTP_CLIENT.get_headers(url)['code']
        if self.robots_exists(resp_code):
            self.parse_txt_data(self.HTTP_CLIENT.get_content(url))

    def parse_txt_data(self, robots):
        """
        parse robots.txt content by lines and fill allow and disallow arrays
        @param robots: content robots.txt
        """
        robots_info = robots['content'].decode(robots['encoding'])
        for line in robots_info:
            self.parse_user_agent(line)
            if self.parse_rules_flag:
                url = urljoin(self.general_url.baseurl,
                              line.split(': ')[1].split(' ')[0])
                if line.startswith(self.disallow_syntax):
                    self.disallow_links.append(url)
                elif line.startswith(self.allow_syntax):
                    self.allow_links.append(url)

    @staticmethod
    def robots_exists(resp_code):
        """
        chekc is robots exists on site
        @param resp_code: response code
        @return bool
        """
        return resp_code == 200

    def parse_user_agent(self, line):
        """
        parse if user agent is *
        @param line: line from robot.txt
        @return bool
        """
        if line.startswith('User-agent: '):
            self.parse_rules_flag = False
        if line.startswith(self.user_agent):
            self.parse_rules_flag = True
