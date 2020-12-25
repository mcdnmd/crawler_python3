"""@package crawler
Documentation for crawler module.

Module responsible for crawler conveyor logic.
"""

import logging
from urllib import robotparser
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from modules.PageParser import PageParser
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
        self.folder = folder
        self.max_depth = depth
        self.CHUNK_SIZE = 1024
        self.current_depth = 0
        self.workers = max_threads
        self.visited = set()
        self.url_queue = []
        self.filters = filters
        self.PageParser = PageParser(self.general_url, self.visited)
        self.StateHandler = state_handler
        self.RobotsHandler = robotparser.RobotFileParser()
        self.HTTPClient = HTTPClient(5)
        self.FileSystemHandler = FileSystemHandler()

    def run(self):
        """
        launch crawler conveyor
        """
        logging.getLogger().setLevel(logging.INFO)
        self.StateHandler.initialize(self)
        self.url_queue.append(self.general_url.URL)
        self.start_conveyor()

    def start_conveyor(self):
        """
        process queries from main queue
        """
        self.upload_crawling_rules()
        logging.info('Crawler was started')
        while self.url_queue and self.current_depth < self.max_depth:
            futures = self.get_futures_pull()
            self.execute_pull_tasks(futures)
            self.current_depth += 1
            self.StateHandler.fill_json_fields(True)
        self.StateHandler.fill_json_fields(False)

    # TODO implement update option
    def get_futures_pull(self):
        """
        get concurrent.futures execute task pull
        @return list of future
        """
        futures = {}
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            current_workers = 0
            while self.url_queue and current_workers < self.workers:
                request_url = self.url_queue.pop(0)
                if not self.is_url_allow(request_url):
                    continue
                future = pool.submit(self.get_website_data, request_url)
                futures[future] = request_url
                current_workers += 1
        return futures

    def execute_pull_tasks(self, futures):
        """
        execute tasks from pool
        """
        for f in futures:
            current_url = futures[f]
            try:
                data = f.result()
            except Exception as e:
                logging.error(f'{current_url} generated an exception '
                              f'while request data: {e}')
            else:
                self.process_data_response(data)

    def process_data_response(self, data):
        """
        define content type and launch parsing methods
        @param data: response dictionary
        """
        self.PageParser.LinkParser.hard_reset()
        if data['code'] == 200:
            content_type, file_extension = self.define_content_type(data)
            if content_type == 'text':
                self.process_html_content(data)
            elif file_extension in self.filters:
                self.process_filtered_content(data, file_extension)

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

    def process_filtered_content(self, data, file_extension):
        """
        processing assets data. Starts uploading file content
        @param data: http response dictionary
        @param file_extension: asset extension
        """
        asset = data['content']
        if self.check_asset_size(data['headers']['Content-Length'],
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
        self.RobotsHandler.set_url(self.create_url('robots.txt'))
        self.RobotsHandler.read()

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
        except KeyError:
            raise
        return content_type[0], content_type[1]

    def add_parsed_links_in_queue(self, links):
        """
        add parsed links in url queue
        """
        if links is not None:
            for url in links:
                if url not in self.visited and url not in self.url_queue:
                    self.url_queue.append(url)

    # TODO: check functionality!
    def upload_page(self, content, url):
        """
        call filesystem handler for page uploading
        @param content: Encoded page content
        @param url: URL class of downloaded content
        """
        self.FileSystemHandler.upload_in_filesystem(self.folder, content, url)

    def upload_asset(self, content, url):
        """
        call filesystem handler for asset uploading
        @param content: asset bytes
        @param url: URL class of downloaded asset
        """
        self.FileSystemHandler.upload_in_filesystem(self.folder, content, url)

    def is_url_allow(self, url):
        """
        check if url is prohibited by robots.txt
        @param url: url via string
        @return bool
        """
        return self.RobotsHandler.can_fetch("*", url)

    def check_asset_size(self, length, file_extension):
        return self.filters[file_extension] == -1 or int(length) <= int(
            self.filters[file_extension])
