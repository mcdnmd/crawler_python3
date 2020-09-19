"""@package safe_states
Documentation for safe_states module.

Module responsible for saving crawler current properties.
"""


import os
import json
import logging
from modules.crawler import Crawler


class Url:
    """
    data structure
    """
    def __init__(self, protocol, netloc, path):
        """
        constructor
        @param protocol: HTTP or HTTPS protocol
        @param netloc: URL netloc
        @param path:  URL path
        """
        self.scheme = protocol
        self.netloc = netloc
        self.path = path


class SetEncoder(json.JSONEncoder):
    """
    JSON special encoder
    """
    def default(self, obj):
        """
        convert obj into JSON list
        @param obj: object with data
        @return list of parameters
        """
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class StateHandler:
    """
    saving and loading crawler properties
    """
    def __init__(self, folder_path):
        """
        the constructor
        """
        self.crawler = None
        self.crawler_fields = None
        self.PATH = folder_path
        self.filename = os.path.join(folder_path, "swopstate.json")

    def initialize(self, crawler):
        """
        initialize crawler
        @param crawler: crawler handler
        """
        self.crawler = crawler

    def fill_swopstate_fields(self, state):
        """
        safe current values of main crawler properties
        @param state: boolean flag for saving data
        """
        if state is True:
            self.crawler_fields = {
                "needSwop": True,
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
                "needSwop": False
            }
        self.safe_state()

    def safe_state(self):
        """
        write crawler properties into JSON dump in OS file system
        """
        with open(self.filename, 'w') as dump_file:
            json.dump(self.crawler_fields, dump_file, cls=SetEncoder)

    def load_crawler_state(self):
        """
        load crawler properties from JSON dump
        @return dictionary contains of crawler properties
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as dump_file:
                self.crawler_fields = json.load(dump_file)
            logging.info("Crawler swopstate.json was loaded")
            return self.crawler_fields
        else:
            self.fill_swopstate_fields(False)
            logging.info("New swopstate.json was created")

    def get_crawler_from_dump(self):
        """
        create crawler with properties
        @return Crawler handler
        """
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
