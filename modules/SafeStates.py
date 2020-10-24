"""@package safe_states
Documentation for safe_states module.

Module responsible for saving crawler current properties.
"""


import os
import json
import logging

from urllib.parse import urljoin
from modules.HTTPClient import Url
from modules.Crawler import Crawler


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
        self.filename = os.path.join(folder_path, "swapstate.json")

    def initialize(self, crawler):
        """
        initialize crawler
        @param crawler: crawler handler
        """
        self.crawler = crawler

    def fill_swapstate_fields(self, flag):
        """
        safe current crawler properties values
        @param flag: boolean flag for saving data
        """
        if flag is True:
            self.crawler_fields = {
                "needSwap": True,
                "fields": {
                    "protocol": self.crawler.general_url.scheme,
                    "netloc": self.crawler.general_url.netloc,
                    "path": self.crawler.general_url.path,
                    "folder": self.crawler.FOLDER,
                    "max_depth": self.crawler.MAX_DEPTH,
                    #"chunk_size": self.crawler.CHUNK_SIZE,
                    "current_depth": self.crawler.current_depth,
                    "workers": self.crawler.workers,
                    "visited": self.crawler.visited,
                    "queue": self.crawler.url_queue,
                    "filters": self.crawler.FILTER_SET}
            }
        else:
            self.crawler_fields = {
                "needSwap": False
            }
        self.safe_state()

    def create_an_empty_swap_state(self):
        """
        "cold" boot creation a JSON structure
        """
        self.crawler_fields = {"needSwap": False}
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
            logging.info("Crawler swapstate.json was loaded")
        else:
            self.create_an_empty_swap_state()
            logging.info("New swapstate.json was created")
        return self.crawler_fields

    def get_crawler_from_dump(self):
        """
        create crawler with properties
        @return Crawler handler
        """
        fields = self.crawler_fields['fields']
        url = urljoin(fields['protocol'] + '://' + fields['netloc'],
                      fields['path'])
        folder = fields['folder']
        depth = fields['max_depth']
        current_depth = fields['current_depth']
        visited = set(fields['visited'])
        #chunk_size = fields['chunk_size']
        max_threads = fields['workers']
        queue = fields['queue']
        filters = fields['filters']
        c = Crawler(url, folder, depth, max_threads, filters, self)
        c.url_queue = queue
        c.current_dept = current_depth
        c.visited = visited
        return c
