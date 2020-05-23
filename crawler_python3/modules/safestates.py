import os
import json
import logging
from modules.crawler import Crawler


class Url:
    def __init__(self, protocol, netloc, path):
        self.scheme = protocol
        self.netloc = netloc
        self.path = path


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class StateHandler:
    def __init__(self):
        self.crawler = None
        self.crawler_fields = None
        self.PATH = os.path.abspath('startup.py' + '/..') + "\\"

    def initialize(self, crawler):
        self.crawler = crawler

    def safe_crawler_state(self, state):
        if state is True:
            self.crawler_fields = {
                "inProcessFlag": True,
                "fields": {
                    "protocol": self.crawler.protocol,
                    "netloc": self.crawler.netloc,
                    "path": self.crawler.path,
                    "folder": self.crawler.FOLDER,
                    "max_depth": self.crawler.MAX_DEPTH,
                    "current_depth": self.crawler.current_depth,
                    "visited": self.crawler.visited,
                    "chunk_size": self.crawler.CHUNK_SIZE,
                    "queue": self.crawler.queue,
                    "simple_filter": self.crawler.simple_filter}
            }
        else:
            self.crawler_fields = {
                "inProcessFlag": False,
                "fields": {}
            }
        self.safe_state()

    def safe_state(self):
        with open(self.PATH + 'dump.json', 'w') as dump_file:
            json.dump(self.crawler_fields, dump_file, cls=SetEncoder)

    def load_crawler_state(self):
        try:
            with open(self.PATH + 'dump.json', 'r') as dump_file:
                self.crawler_fields = json.load(dump_file)
            return self.crawler_fields
        except Exception as exc:
            logging.error('Generated an exception while load dump: %s' % exc)
            return None

    def load_crawler_from_dump(self):
        fields = self.crawler_fields['fields']
        url = Url(fields['protocol'],
                  fields['netloc'],
                  fields['path'])
        folder = fields['folder']
        depth = fields['max_depth']
        current_depth = fields['current_depth']
        visited = set(fields['visited'])
        chunk_size = fields['chunk_size']
        queue = fields['queue']
        simple_filter = fields['simple_filter']
        c = Crawler(url, folder, depth, chunk_size, simple_filter, self)
        c.queue = queue
        c.current_dept = current_depth
        c.visited = visited
        return c
