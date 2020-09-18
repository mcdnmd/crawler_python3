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
        self.technical_syntax = 'Disallow'
        self.parse_rules = False

    def get_strict_rules(self, txt):
        """
        get rules Disallow from server
        @param txt robots.txt file content
        @return list of urls
        """
        return self.parse_txt_data(txt)

    def parse_txt_data(self, robots):
        result = []
        for line in robots.split('\n'):
            if line.startswith('User-agent: '):
                self.parse_rules = False
            if line.startswith(self.user_agent):
                self.parse_rules = True
            if self.parse_rules and line.startswith(self.technical_syntax):
                result.append(line.split(': ')[1].split(' ')[0])
        return result
