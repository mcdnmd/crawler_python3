"""@package FileSystemHandler
Documentation for FileSystemHandler module.

Module responsible for working with OS file system
"""


import logging
import os
import re
from pathlib import Path


class FileSystemHandler:
    """
    release methods for File System communication
    """
    def __init__(self):
        self.WEB_FILE_FORMAT = re.compile(r'')

    def upload_in_filesystem(self, folder, path, data):
        """
        Upload data in chosen folder
        @param folder: root application folder
        @param path: relative file path
        @param data: file content
        """
        filename = self.generate_absolute_path(folder, path)
        try:
            with open(f'{filename}', 'w+') as f:
                f.write(data['content'])
        except Exception as exc:
            logging.error(f'{path} generated an exception while save page:'
                          f' {exc}')
        else:
            logging.info(f'{path} successfully download')

    #   TODO add regular expr to define folder not other files .php .img etc.
    def generate_absolute_path(self, folder, path):
        """
        generate absolute path for different OS
        @param folder: root application folder
        @param path: relative file path
        @return absolute filename
        """
        self.ping_directory(folder, path)
        if os.path.basename(path) == '':
            path += 'index.html'
        if path.startswith('/'):
            path = path[1:]
        return os.path.join(folder, path)

    def ping_directory(self, folder, webpage_path):
        abs_path = folder + os.path.dirname(webpage_path)
        if not os.path.exists(abs_path):
            self.create_directory(abs_path)
            logging.info(f'Creating folder {abs_path}')
            return
        logging.info(f'Directory {abs_path} already exists')

    def create_directory(self, abs_path):
        """
        create new folder if it`s not existed
        @param abs_path:
        :return:
        """
        os.mkdir(abs_path)

