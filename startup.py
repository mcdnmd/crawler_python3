"""@package startup
Documentation for startup module.

This is a main module to prepare environment and launch crawler conveyor
"""
import random
import string

ERROR_PYTHON_VERSION = 3

import sys

if sys.version_info < (3, 8):
    print('Use python >= 3.8', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse
import os
from urllib.parse import urlparse
from modules.crawler import Crawler
from modules.safe_states import StateHandler


def dir_path(folder):
    """
    check if directory is exist
    @param folder string name
    @return string path
    """
    if os.path.exists(folder):
        return str(folder)
    else:
        raise NotADirectoryError(folder)


def wed_url(url):
    """
    parse url string
    @param url: any url or ip-address of site
    @return cortege with scheme, netloc and path
    """
    result = urlparse(url)
    if all([result.scheme, result.netloc]):
        return result
    else:
        raise ValueError(url)


def get_random_folder_name():
    """
    generate random folder name
    @return string folder name
    """
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits) for _ in range(8))


def get_terminal_arguments():
    """
    parse terminal input arguments
    @return arguments
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
        default=os.path.join(os.getcwdb().decode(), get_random_folder_name()),
        help="save folder")
    parser.add_argument(
        '-th',
        type=int,
        action="store",
        dest="max_threads",
        default=1,
        help="maximal number of threads")
    parser.add_argument(
        '-d',
        type=int,
        action="store",
        dest="depth",
        default=5,
        help="maximal depth for site tree")
    parser.add_argument(
        '-ef',
        type=int,
        action="store",
        dest="simple_filter",
        default=['.png', '.jpg', 'jpeg', '.gif'],
        help="extension filter")
    return parser.parse_args()


def main():
    """
    start crawling utility
    """
    args = get_terminal_arguments()

    stateHandler = StateHandler(args.folder)
    swop_state = stateHandler.load_crawler_state()

    if swop_state is not None and swop_state['needSwop'] is True:
        crawler = stateHandler.get_crawler_from_dump()
    else:
        crawler = Crawler(args.url,
                          args.folder,
                          args.depth,
                          args.max_threads,
                          args.simple_filter,
                          StateHandler(args.folder))
    crawler.run()


if __name__ == '__main__':
    main()
