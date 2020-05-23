ERROR_PYTHON_VERSION = 3

import sys

if sys.version_info < (3, 7):
    print('Use python >= 3.7', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse
import os
from urllib.parse import urlparse
from modules.crawler import Crawler
from modules import safestates


def dir_path(string):
    if os.path.isdir(string):
        return str(string)
    else:
        raise NotADirectoryError(string)


def wed_url(string):
    result = urlparse(string)
    if all([result.scheme, result.netloc, result.path]):
        return result
    else:
        raise ValueError(string)


def main():
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

    dump = safestates.load_crawler_state()
    if dump is not None and dump['inProcessFlag'] is True:
        c = safestates.load_crawler_from_dump(dump)
    else:
        c = Crawler(args.url,
                    args.folder,
                    args.depth,
                    args.chunk_size,
                    args.simple_filter)
    c.run()


if __name__ == '__main__':
    main()
