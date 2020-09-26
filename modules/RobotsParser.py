"""@package robots_parser
Documentation for robots_parser module.

Module responsible for defining crawling rules
"""


class RobotsParser:
    """
    parser robots.txt files
    """
    def __init__(self):
        self.user_agent = 'User-agent: *'
        self.disallow_syntax = 'Disallow'
        self.allow_syntax = 'Allow'
        self.allow_links = []
        self.disallow_links = []
        self.parse_rules = False
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
            self.parse_txt_data(self.HTTP_CLIENT.get_content(url)['content'])

    # TODO make parsing easy!
    def parse_txt_data(self, robots):
        for line in robots.split('\n'):
            if line.startswith('User-agent: '):
                self.parse_rules = False
            if line.startswith(self.user_agent):
                self.parse_rules = True
            if self.parse_rules and line.startswith(self.disallow_syntax):
                self.disallow_links.append(line.split(': ')[1].split(' ')[0])
            elif self.parse_rules and line.startswith(self.allow_syntax):
                self.allow_links.append(line.split(': ')[1].split(' ')[0])

    def robots_exists(self, resp_code):
        return resp_code == 200
