import os
import shutil
import socket
import unittest
from http.client import HTTPResponse
from unittest import mock

from startup import choose_script

URL = 'https://test.org'
PATH = os.path.join(os.path.dirname(__file__), 'site')
FOLDER = os.path.join(os.path.dirname(__file__), "dump")
FILTERS = {'css': -1, 'js': -1, 'xml': -1, 'png': 900, 'jpg': 850}
DOWNLOADED_SIDE_EFFECTS = []
UPDATED_SIDE_EFFECTS = []
FOLDER_DATA = [str(os.path.join(FOLDER, 'index.html')),
               str(os.path.join(FOLDER, 'main_page.html')),
               str(os.path.join(FOLDER, 'styles/style.css')),
               str(os.path.join(FOLDER, 'pics/allow/compass.png')),
               str(os.path.join(FOLDER, 'image/mountain.png')),
               str(os.path.join(FOLDER, 'image/shopping.jpg')),
               str(os.path.join(FOLDER, 'currentstate.json'))]

with open(os.path.join(PATH, "robots.txt")) as file:
    ROBOTS_TXT = bytes(file.read().encode("utf-8"))


class CrawlerTestLogic(unittest.TestCase):
    def setUp(self):
        self.fill_downloaded_side_effects()
        self.fill_update_side_effects()

    @mock.patch("modules.HTTPClient.HTTPClient.make_request",
                side_effect=DOWNLOADED_SIDE_EFFECTS)
    @mock.patch("urllib.request.urlopen",
                return_value=HTTPResponse(sock=socket.socket()))
    @mock.patch("http.client.HTTPResponse.read", return_value=ROBOTS_TXT)
    def test_correctly_downloaded_content(self, mock_1, mock_2, mock_3):
        os.makedirs(FOLDER, exist_ok=True)
        self.crawler = choose_script(FOLDER, False, URL, 3, 4, FILTERS)
        self.crawler.run()
        result = []
        self.show_folder(FOLDER, result)
        self.assertSetEqual(set(FOLDER_DATA), set(result))

    @mock.patch("modules.HTTPClient.HTTPClient.make_request",
                side_effect=UPDATED_SIDE_EFFECTS)
    @mock.patch("urllib.request.urlopen",
                return_value=HTTPResponse(sock=socket.socket()))
    @mock.patch("http.client.HTTPResponse.read", return_value=ROBOTS_TXT)
    def test_update_content_correctly(self, mock_1, mock_2, mock_3):
        self.crawler = choose_script(FOLDER, True, URL, 3, 4, FILTERS)
        self.crawler.update('Mon, 23 Dec 2020 03:27:10 GMT')
        size = os.path.getsize(os.path.join(FOLDER, 'index.html'))
        size_required = os.path.getsize(
            os.path.join(os.path.dirname(__file__),
                         'site/updatedsite/index.html'))
        shutil.rmtree(FOLDER)
        self.assertEqual(size_required, size)

    def fill_downloaded_side_effects(self):
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_text(200, "index.html", URL + "/index.html",
                                "text/html", 1024, "utf-8"))
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_text(200, "styles/style.css",
                                URL + "/styles/style.css", "text/css", 1024,
                                "utf-8"))
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_text(200, "main_page.html", URL + "/main_page.html",
                                "text/html", 1500, "utf-8"))
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_asset(200, "image/shopping.jpg",
                                 URL + "/image/shopping.jpg", "image/jpg", 800,
                                 "utf-8"))
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_asset(200, "image/food.png",
                                 URL + "/image/food.png", "image/png", 1100,
                                 "utf-8"))
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_asset(200, "image/mountain.png",
                                 URL + "/image/mountain.png", "image/png", 690,
                                 "utf-8"))
        DOWNLOADED_SIDE_EFFECTS.append(
            self.get_reply_asset(200, "pics/allow/compass.png",
                                 URL + "/pics/allow/compass.png", "image/png",
                                 880, "utf-8"))

    def fill_update_side_effects(self):
        UPDATED_SIDE_EFFECTS.append(
            self.get_reply_update_text(200, "styles/style.css",
                                       URL + "/styles/style.css", "text/css",
                                       1024, "utf-8", True,
                                       "Fri, 31 Dec 1998 13:37:00 GMT"))
        UPDATED_SIDE_EFFECTS.append(self.get_reply_update_text(500))
        UPDATED_SIDE_EFFECTS.append(self.get_reply_update_text(500))
        UPDATED_SIDE_EFFECTS.append(
            self.get_reply_update_text(200, "updatedsite/index.html",
                                       URL + "/index.html", "text/html", 1024,
                                       "utf-8", True,
                                       "Fri, 20 Dec 3000 13:37:00 GMT"))
        UPDATED_SIDE_EFFECTS.append(self.get_reply_update_text(500))
        UPDATED_SIDE_EFFECTS.append(self.get_reply_update_text(500))

    @staticmethod
    def get_reply_text(code, filename, url, type_str, content_len, encoding):
        if code != 200:
            return {"url": url, "code": code}
        with open(os.path.join(PATH, filename), 'r') as data:
            tmp_dict = {"url": url, "code": code, "type": type_str,
                        "headers": {'Content-Length': content_len},
                        "content": bytes(data.read().encode(encoding)),
                        "encoding": encoding}
            return tmp_dict

    @staticmethod
    def get_reply_asset(code, filename, url, type_str, content_len, encoding):
        if code != 200:
            return {"url": url, "code": code}
        with open(os.path.join(PATH, filename), 'r') as data:
            tmp_dict = {"url": url, "code": code, "type": type_str,
                        "headers": {'Content-Length': content_len},
                        "content": data.buffer.read(), "encoding": encoding}
            return tmp_dict

    def get_reply_update_text(self, code, filename='', url='', type_str='',
                              content_len=0, encoding='',
                              add_last_modify_field=False, date=''):
        tmp_dict = self.get_reply_text(code, filename, url, type_str,
                                       content_len, encoding)
        if add_last_modify_field:
            tmp_dict['headers']['Last-Modified'] = date
        return tmp_dict

    def get_reply_update_asset(self, code, filename='', url='', type_str='',
                               content_len=0, encoding='',
                               add_last_modify_field=False, date=''):
        tmp_dict = self.get_reply_asset(code, filename, url, type_str,
                                        content_len, encoding)
        if add_last_modify_field:
            tmp_dict['headers']['Last-Modified'] = date
        return tmp_dict

    def show_folder(self, folder, result):
        for path in os.listdir(folder):
            abs_path = os.path.join(folder, path)
            if os.path.isdir(abs_path):
                self.show_folder(abs_path, result)
            else:
                result.append(abs_path)
