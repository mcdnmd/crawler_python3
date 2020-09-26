"""@package crawler
Documentation for crawler module.

Module responsible for crawler conveyor logic.
"""

import os
import logging
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from modules.PageParser import PageParser
from modules.RobotsParser import RobotsParser
from modules.HTTPClient import HTTPClient
from modules.FileSystemHandler import FileSystemHandler


class Crawler:
    """
    release main conveyor
    """

    def __init__(self,
                 url,
                 folder,
                 depth,
                 max_threads,
                 state_handler):
        """
        the constructor
        @param url: dictionary with scheme, netloc and path of URL
        @param folder: folder for saving downloaded pages
        @param depth: maximal depth
        @param max_threads: maximum number of threads
        @param state_handler: program state handler
        """
        self.protocol = url.scheme
        self.netloc = url.netloc
        self.path = url.path
        self.FOLDER = folder
        self.MAX_DEPTH = depth
        self.CHUNK_SIZE = 1024
        self.current_depth = 0
        self.workers = max_threads
        self.visited = set()
        self.url_queue = []
        self.PageParser = None
        self.StateHandler = state_handler
        self.RobotsParser = RobotsParser()
        self.HTTPClient = HTTPClient(2)
        self.FileSystemHandler = FileSystemHandler()
        logging.warning('Crawler was started')

    def run(self):
        """
        launch crawler conveyor
        """
        link = self.create_url(self.path)
        self.StateHandler.initialize(self)
        self.RobotsParser.initialize(self.HTTPClient)
        self.PageParser = PageParser(self.protocol,
                                     self.netloc,
                                     self.visited)
        self.url_queue.append(link)
        self.start_conveyor()

    # TODO implement robots.txt
    def start_conveyor(self):
        """
        process queries from main queue
        """
        self.upload_rules()
        logging.info('Crawler`s conveyor was started')
        while self.url_queue and self.current_depth < self.MAX_DEPTH:
            futures = self.get_futures_pull()
            self.execute_pull_tasks(futures)
            self.current_depth += 1
            self.StateHandler.fill_swopstate_fields(True)
            logging.warning("crawler safe current state")
        self.StateHandler.fill_swopstate_fields(False)

    def get_website_data(self, url):
        """
        make HTTP or HTTPS requests
        @param url: site URL or IP address
        @return dictionary with content and page encoding
        """
        return self.HTTPClient.get_content(url)

    def get_robots_data(self, url):
        response = self.HTTPClient.get_headers(url)
        if response['code'] == 200:
            return response['headers']
        return None

    def upload_rules(self):
        logging.info('Try to get robots.txt')
        self.RobotsParser.get_rules(self.create_url('robots.txt'))

    def create_url(self, path):
        """
        concatenating scheme, netloc and path into URL address
        @param path: on site page position
        @return string URL
        """
        return urljoin(self.protocol + '://' + self.netloc, path)

    # TODO implement update feature
    def get_futures_pull(self):
        """
        get concurrent.futures execute task pull
        @return list of future
        """
        futures = {}
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            while self.url_queue:
                request_url = self.url_queue.pop()
                future = pool.submit(self.get_website_data, request_url)
                futures[future] = request_url
        logging.info('Task pull created')
        return futures

    def execute_pull_tasks(self, futures):
        """
        execute tasks from pull
        """
        logging.info('Start executing tasks')
        for f in futures:
            self.PageParser.LinkParser.hard_reset()
            current_url = futures[f]
            try:
                data = f.result()
            except Exception as e:
                logging.error(f'{current_url} generated an exception while '
                              f'request data: {e}')
            else:
                self.add_parsed_links_in_queue(
                    self.PageParser.get_filtered_links(data['content']))
                self.download_page(futures[f], data)
                self.visited.add(data['url'])

    def add_parsed_links_in_queue(self, links):
        """
        add parsed links in url queue
        """
        if links is not None:
            for url in links:
                self.url_queue.append(url)

    # TODO: check functionality!
    def download_page(self, url, data):
        """
        call filesystem handler for page uploading
        @param url: URL address of downloaded content
        @param data: dictionary with content and encoding
        """
        path = urlparse(url).path
        self.FileSystemHandler.upload_in_filesystem(self.FOLDER, path, data)
