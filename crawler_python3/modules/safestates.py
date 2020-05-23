import json
import logging
from modules.crawler import Crawler


class Url:
    def __init__(self, protocol, netloc, path):
        self.scheme = protocol
        self.netloc = netloc
        self.path = path


def safe_crawler_state(crawler, state):
    if state is True:
        crawler_fields = {
            "inProcessFlag": True,
            "fields": {
                "protocol": crawler.protocol,
                "netloc": crawler.netloc,
                "path": crawler.path,
                "folder": crawler.FOLDER,
                "max_depth": crawler.MAX_DEPTH,
                "chunk_size": crawler.CHUNK_SIZE,
                "queue": crawler.queue,
                "simple_filter": crawler.simple_filter}
        }
    else:
        crawler_fields = {
            "inProcessFlag": False,
            "fields": {}
        }
    with open('dump.json', 'w+') as dump_file:
        json.dump(crawler_fields, dump_file)


def load_crawler_state():
    try:
        dump_file = open('dump.json')
        crawler_fields = json.load(dump_file)
        return crawler_fields
    except Exception as exc:
        logging.error('Generated an exception while load dump: %s' % exc)
        return None


def load_crawler_from_dump(dump):
    url = Url(dump['protocol'], dump['netloc'], dump['path'])
    folder = dump['folder']
    depth = dump['max_depth']
    chunk_size = dump['chunk_size']
    queue = dump['queue']
    simple_filter = ['simple_filter']
    c = Crawler(url, folder, depth, chunk_size, simple_filter)
    c.queue = queue
    return c
