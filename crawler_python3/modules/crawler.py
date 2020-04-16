import os
from queue import Queue
from modules import page, request
import startup


class Crawler:
    def __init__(self, link, dir):
        self.MAX_DEPTH = startup.MAX_DEPTH
        self.link = link
        self.dir = dir
        self.pages = Queue()
        self.RequestHANDLER = request.Request()
        self.CurrentPage = None

    def run(self):
        os.chdir(self.dir)
        self.pages.put(page.Page(self.link, 0))
        self.crawler_loop()

    def crawler_loop(self):
        while self.pages.qsize() != 0:
            page = self.pages.get()
            self.CurrentPage = page
            self.CurrentPage.load_content(self.get_content(self.CurrentPage.link))
            if self.CurrentPage.response is not None:
                self.CurrentPage.create_filename()
                self.download_content()
                self.CurrentPage.extract_links()
                self.queue_merge()

    def get_content(self, page):
        return self.RequestHANDLER.send_request(page)

    def queue_merge(self):
        for page in self.CurrentPage.possible_pages:
            self.pages.put(page)

    def download_content(self):
        file = open(self.CurrentPage.filename, "w+")
        for chunk in self.CurrentPage.response.iter_content(chunk_size=512):
            file.write(chunk.decode("cp1251", errors='ignore'))
        file.close()
