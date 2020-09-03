"""@package startup
Documentation for startup module.

This is a main module to prepare environment and launch crawler conveyor
"""

ERROR_PYTHON_VERSION = 3

import sys

if sys.version_info < (3, 8):
    print('Use python >= 3.8', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse
import os
from urllib.parse import urlparse
from modules.crawler import Crawler
from modules.safestates import StateHandler


def dir_path(string):
    """
    check if directory is exist
    @param string directory path
    @return string path
    """
    if os.path.isdir(string):
        return str(string)
    else:
        raise NotADirectoryError(string)


def wed_url(string):
    """
    parse url string
    @param string: any url or ip-address of site
    @return cortege with scheme, netloc and path
    """
    result = urlparse(string)
    if all([result.scheme, result.netloc, result.path]):
        return result
    else:
        raise ValueError(string)


def main():
    """
    parse commands from terminal and start or continue crawling site
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        type=wed_url,
        action="store",
        help="site url or ip-address")
    parser.add_argument(
        '-f',
        type=dir_path,
        action="store",
        dest="folder",
        default=os.getcwdb().decode())
    parser.add_argument(
        '-s',
        type=int,
        action="store",
        dest="chunk_size",
        default=512)
    parser.add_argument(
        '-d',
        type=int,
        action="store",
        dest="depth",
        default=5,
        help="maximal depth for crawler tree")
    parser.add_argument(
        '-ef',
        type=int,
        action="store",
        dest="simple_filter",
        default=['.png', '.jpg', 'jpeg', '.gif'],
        help="extension filter")

    args = parser.parse_args()

    stateHandler = StateHandler()
    dump = stateHandler.load_crawler_state()
    if dump is not None and dump['inProcessFlag'] is True:
        crawler = stateHandler.load_crawler_from_dump()
    else:
        crawler = Crawler(args.url,
                          args.folder,
                          args.depth,
                          args.chunk_size,
                          args.simple_filter,
                          StateHandler())
    crawler.run()


if __name__ == '__main__':
    main()
