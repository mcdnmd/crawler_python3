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

    def upload_in_filesystem(self, folder, content, url):
        """
        Upload data in chosen folder
        @param folder: root application folder
        @param content: file content
        @param url: URL class address
        """
        abs_dir_path = folder + url.dirname
        abs_filename = os.path.join(abs_dir_path, url.filename)
        os.makedirs(abs_dir_path, exist_ok=True)
        try:
            if isinstance(content, type(b'')):
                self.upload_asset(abs_filename, content)
            else:
                self.upload_page(abs_filename, content)
        except Exception as exc:
            logging.error(
                f' {abs_filename} generated an exception while save file'
                f' {exc}')
        else:
            logging.info(f' {abs_filename} successfully download')

    def ping_directory(self, abs_dir_path):
        """
        ping directory. If such folder not exists - create
        @param abs_dir_path: string absolute dir path on server
        """
        if not os.path.exists(abs_dir_path):
            self.create_directory(abs_dir_path)
            logging.info(f' Creating folder {abs_dir_path}')
            return
        logging.info(f' Directory {abs_dir_path} exists')

    @staticmethod
    def create_directory(abs_path):
        """
        create new folder if it`s not existed
        @param abs_path: path to directory
        """
        Path(abs_path).mkdir(parents=True)

    @staticmethod
    def upload_page(filename, content):
        with open(f'{filename}', 'w') as f:
            f.write(content)

    @staticmethod
    def upload_asset(filename, content):
        with open(f'{filename}', 'wb') as f:
            f.write(content)
