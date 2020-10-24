"""@package crawler
Documentation for crawler module.

Module responsible for crawler conveyor logic.
"""

import os
import logging
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from modules.PageParser import PageParser
from modules.RobotsHandler import RobotsParser
from modules.HTTPClient import HTTPClient
from modules.FileSystemHandler import FileSystemHandler

from modules.Url import Url


class Crawler:
    """
    release main conveyor
    """

    def __init__(self, str_url, folder, depth, max_threads, filters,
                 state_handler):
        """
        the constructor
        @param str_url: string URL
        @param folder: folder for saving downloaded pages
        @param depth: maximal depth
        @param max_threads: maximum number of threads
        @param state_handler: program state handler
        """
        self.general_url = Url(str_url)
        self.FOLDER = folder
        self.MAX_DEPTH = depth
        self.CHUNK_SIZE = 1024
        self.current_depth = 0
        self.workers = max_threads
        self.visited = set()
        self.url_queue = []
        self.FILTER_SET = filters
        self.PageParser = PageParser(self.general_url, self.visited)
        self.StateHandler = state_handler
        self.RobotsParser = RobotsParser(str_url)
        self.HTTPClient = HTTPClient(5)
        self.FileSystemHandler = FileSystemHandler()
        logging.warning('Crawler was started')

    def run(self):
        """
        launch crawler conveyor
        """
        logging.getLogger().setLevel(logging.INFO)
        self.StateHandler.initialize(self)
        self.RobotsParser.initialize(self.HTTPClient)
        self.url_queue.append(self.general_url.URL)
        self.start_conveyor()

    def start_conveyor(self):
        """
        process queries from main queue
        """
        self.upload_crawling_rules()
        logging.info('Crawler conveyor was started')
        while self.url_queue and self.current_depth < self.MAX_DEPTH:
            futures = self.get_futures_pull()
            self.execute_pull_tasks(futures)
            self.current_depth += 1
            self.StateHandler.fill_swapstate_fields(True)
            logging.info("crawler safe current state")
        self.StateHandler.fill_swapstate_fields(False)
        return None

    # TODO implement update option
    def get_futures_pull(self):
        """
        get concurrent.futures execute task pull
        @return list of future
        """
        futures = {}
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            while self.url_queue:
                request_url = self.url_queue.pop()
                if self.is_url_disallow(request_url):
                    continue
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
                logging.error(f'{current_url.URL} generated an exception '
                              f'while request data: {e}')
            else:
                self.process_data_response(data)

    def process_data_response(self, data):
        """
        define content type and launch parsing methods
        @param data: response dictionary
        """
        content_type, file_extension = self.define_content_type(data)
        if content_type == 'text':
            self.process_html_content(data)
        elif file_extension in self.FILTER_SET:
            self.process_filter_content(data, file_extension)

    def process_html_content(self, data):
        """
        processing html data. Extract links and upload content
        @param data: http response dictionary
        """
        content = data['content'].decode(data['encoding'])
        self.add_parsed_links_in_queue(
            self.PageParser.get_filtered_links(content))
        self.upload_page(content, Url(data['url']))
        self.visited.add(data['url'])

    def process_filter_content(self, data, file_extension):
        """
        processing assets data. Starts uploading file content
        @param data: http response dictionary
        @param file_extension: asset extension
        """
        asset = data['content']
        if self.check_asset_size(
                data['headers']['Content-Length'],
                file_extension):
            self.upload_asset(asset, Url(data['url']))
            return
        logging.info(f'Asset {data["url"]} large then available')

    def get_website_data(self, url):
        """
        make HTTP or HTTPS requests
        @param url: site URL or IP address
        @return dictionary with content and page encoding
        """
        return self.HTTPClient.get_content(url)

    def upload_crawling_rules(self):
        """
        launch RobotsParser for getting robots.txt
        @return list of rules
        """
        logging.info('Try to get robots.txt')
        self.RobotsParser.get_rules(self.create_url('robots.txt'))

    def create_url(self, path):
        """
        concatenating scheme, netloc and path into URL address
        @param path: on site page position
        @return string URL
        """
        return urljoin(self.general_url.baseurl, path)

    @staticmethod
    def define_content_type(response):
        """
        define what is url is. Site content, picture or script
        @param response: urllib http response
        @return type of content
        """
        try:
            content_type = response['type'].split(';')[0].split('/')
        except KeyError as e:
            print(response['type'])
            raise
        return content_type[0], content_type[1]

    def add_parsed_links_in_queue(self, links):
        """
        add parsed links in url queue
        """
        if links is not None:
            for url in links:
                self.url_queue.append(url)

    # TODO: check functionality!
    def upload_page(self, content, url):
        """
        call filesystem handler for page uploading
        @param content: Encoded page content
        @param url: URL class of downloaded content
        """
        self.FileSystemHandler.upload_in_filesystem(self.FOLDER, content, url)

    def upload_asset(self, content, url):
        """
        call filesystem handler for asset uploading
        @param content: asset bytes
        @param url: URL class of downloaded asset
        """
        self.FileSystemHandler.upload_in_filesystem(self.FOLDER, content, url)

    def is_url_disallow(self, url):
        """
        check if url is prohibited by robots.txt
        @param url: url via string
        @return bool
        """
        return url in self.RobotsParser.disallow_links and \
               url not in self.RobotsParser.allow_links

    def check_asset_size(self, length, file_extension):
        return self.FILTER_SET[file_extension] == -1 or \
               int(length) <= int(self.FILTER_SET[file_extension])
