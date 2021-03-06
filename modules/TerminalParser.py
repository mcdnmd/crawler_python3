import argparse
import os
import re
from urllib.parse import urlparse
from pathlib import Path


def create_folder(folder):
    """
    safety create a new folder
    @param folder string path
    """
    Path(folder).mkdir(parents=True)


class TerminalParser:
    """
    parse input arguments
    """
    def __init__(self):
        self.default_filters = [['css'], ['js'], ['xml']]
        self.SCHEME_FORMAT = re.compile(
            r"^(http|ftp)s?$",
            re.IGNORECASE
        )

    @staticmethod
    def verify_folder_path(folder):
        """
        check if directory is exist
        @param folder string name
        @return string path
        """
        if os.path.exists(folder):
            return str(folder)
        create_folder(folder)
        if folder.endswith('/'):
            folder = folder[:-1]
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
        return result.geturl()

    @staticmethod
    def parse_filters(filters):
        """
        parsing different filters with size
        @param filters: args
        @return filter dictionary
        """
        result = {}

        for f in filters:
            name = f[0]
            name = name.replace('.', '')
            if len(f) == 2:
                size = f[1]
                result[name] = size
            else:
                result[name] = -1
        return result

    # TODO add update option
    def get_terminal_arguments(self):
        """
        parse terminal input arguments
        @return arguments
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'url',
            type=self.verify_wed_url,
            action="store",
            help="site url or ip-address")
        parser.add_argument(
            '-f',
            '--folder',
            type=self.verify_folder_path,
            action="store",
            dest="folder",
            default=os.getcwd(),
            help="save folder")
        parser.add_argument(
            '-j',
            '--threads',
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
        parser.add_argument(
            '-F',
            '--filter',
            nargs='+',
            action="append",
            dest="filters",
            default=self.default_filters,
            help="add extension filter and size .<file_extension> <size>")
        parser.add_argument(
            '-U',
            '--update',
            action='store_true',
            dest='update_all',
            default=False,
            help='update chose site (required downloaded content in folder)')
        return parser.parse_args()
