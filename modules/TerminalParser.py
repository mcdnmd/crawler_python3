import argparse
import os
import random
import re
import string
from urllib.parse import urlparse


def create_folder(folder):
    """
    safety create a new folder
    @param folder string path
    """
    os.mkdir(folder)


def get_random_folder_name():
    """
    generate random folder name
    @return string folder name
    """
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits) for _ in range(8))


class TerminalParser:
    """
    parse input arguments
    """
    def __init__(self):
        self.SCHEME_FORMAT = re.compile(
            r"^(http|ftp)s?$",
            re.IGNORECASE
        )
        self.NETLOC_FORMAT = re.compile(
            r'(?:^(\w{1,255}):(.{1,255})@|^)'
            r'(?:(?:(?=\S{0,253}(?:$|:))'
            r'((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+'
            r'(?:[a-z0-9]{1,63})))'
            r'|localhost)'
            r'(:\d{1,5})?',
            re.IGNORECASE
        )

    def verify_folder_path(self, folder):
        """
        check if directory is exist
        @param folder string name
        @return string path
        """
        if os.path.exists(folder):
            return str(folder)
        create_folder(folder)
        return str(folder)

    def verify_wed_url(self, url):
        """
        parse url string
        @param url: any url or ip-address of site
        @return cortege with scheme, netloc and path
        """
        if len(url) > 2048:
            raise ValueError(
                f'URL exceeds its maximum length of 2048 characters (given '
                f'{len(url)})')
        result = urlparse(url)
        scheme = result.scheme
        netloc = result.netloc
        if not scheme:
            raise ValueError("No URL scheme specified")
        if not re.fullmatch(self.SCHEME_FORMAT, scheme):
            raise ValueError(
                f"URL scheme must either be http(s) or ftp(s) (given "
                f"{scheme})")
        if not netloc:
            raise ValueError("No URL domain specified")
        if not re.fullmatch(self.NETLOC_FORMAT, netloc):
            raise ValueError(f"URL domain malformed (given {netloc})")
        return result

    # TODO add update option
    # TODO add special file config
    def get_terminal_arguments(self):
        """
        parse terminal input arguments
        @return arguments
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'url',
            type= self.verify_wed_url,
            action="store",
            help="site url or ip-address")
        parser.add_argument(
            '-f',
            type= self.verify_folder_path,
            action="store",
            dest="folder",
            default=os.path.join(os.getcwdb().decode(),
                                 get_random_folder_name()),
            help="save folder")
        parser.add_argument(
            '-th',
            type=int,
            action="store",
            dest="max_threads",
            default=2 * os.cpu_count(),
            help="maximal number of threads")
        parser.add_argument(
            '-d',
            type=int,
            action="store",
            dest="depth",
            default=5,
            help="maximal depth for site tree")
        return parser.parse_args()
