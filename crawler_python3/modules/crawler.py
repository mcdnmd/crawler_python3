import os
import logging
from urllib.request import urlopen
from urllib.parse import urlparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from modules.pageparser import PageParser


class Crawler:
    def __init__(self,
                 url,
                 folder,
                 depth,
                 chunk_size,
                 simple_filter,
                 StateHandler):
        self.protocol = url.scheme
        self.netloc = url.netloc
        self.path = url.path
        self.FOLDER = folder
        self.MAX_DEPTH = depth
        self.CHUNK_SIZE = chunk_size
        self.current_depth = 0
        self.simple_filter = simple_filter
        self.workers = 2 * os.cpu_count()
        self.timeout = 2
        self.visited = set()
        self.queue = []
        self.PageParser = None
        self.StateHandler = StateHandler
        logging.warning('Crawler was started')

    def run(self):
        link = self.make_link(self.path)
        self.StateHandler.initialize(self)
        self.PageParser = PageParser(self.protocol,
                                     self.netloc,
                                     self.simple_filter,
                                     self.visited)
        self.queue.append(link)
        self.conveyor()

    def conveyor(self):
        logging.info('Crawler`s conveyor was started')
        while not len(self.queue) == 0 and self.current_depth < self.MAX_DEPTH:
            futures = {}
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                while not len(self.queue) == 0:
                    request_url = self.queue.pop()
                    future = pool.submit(self.make_request, request_url)
                    futures[future] = request_url
            for f in futures:
                self.PageParser.LinkParser.hard_reset()
                url = futures[f]
                try:
                    data = f.result()
                    paths = self.PageParser.get_filtred_links(data['content'])
                    if paths is not None:
                        for path in paths:
                            self.queue.append(path)
                    self.download_page(url, data)
                except Exception as exc:
                    logging.error('%r generated an exception: %s' % (url, exc))
                else:
                    logging.warning('%r page is %d bytes' % (url, len(data)))
            self.current_depth += 1
            self.StateHandler.safe_crawler_state(True)
        self.StateHandler.safe_crawler_state(False)

    def make_request(self, url):
        with urlopen(url, timeout=self.timeout) as conn:
            encoding = conn.headers.get_content_charset() or 'UTF-8'
            return {"content": conn.read().decode(encoding),
                    "encoding": encoding}

    def make_link(self, path):
        return self.protocol + '://' + self.netloc + path

    def download_page(self, url, data):
        try:
            path = urlparse(url).path.replace('/', '')
            filename = str(Path(self.FOLDER, path))
            with open(f'{filename}', 'w+') as f:
                f.write(str(bytes(data['content'], data['encoding'])))
        except Exception as exc:
            logging.error('%r generated an exception: %s' % (url, exc))
        else:
            logging.warning('%s successfully download' % url)
