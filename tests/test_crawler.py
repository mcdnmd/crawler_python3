import os
import socket
import unittest
import shutil
from unittest import mock
from http.client import HTTPResponse

from modules.Crawler import Crawler
from modules.StateHandler import StateHandler

URL = 'https://test.org'
PATH = os.path.join(os.path.dirname(__file__), 'site')
FOLDER = os.path.join(os.path.dirname(__file__), "dump")
FILTERS = {'css': -1, 'js': -1, 'xml': -1, 'png': 900, 'jpg': 850}
SIDE_EFFECTS = []
FOLDER_DATA = [str(os.path.join(FOLDER, 'index.html')),
               str(os.path.join(FOLDER, 'main_page.html')),
               str(os.path.join(FOLDER, 'styles/style.css')),
               str(os.path.join(FOLDER, 'pics/allow/compass.png')),
               str(os.path.join(FOLDER, 'image/mountain.png')),
               str(os.path.join(FOLDER, 'image/shopping.jpg'))]

with open(os.path.join(PATH, "robots.txt")) as file:
    ROBOTS_TXT = bytes(file.read().encode("utf-8"))


class CrawlerTestLogic(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler(URL, FOLDER, 3, 4, FILTERS,
                               StateHandler(FOLDER))
        self.create_side_effects()

    @mock.patch("modules.HTTPClient.HTTPClient.make_request",
                side_effect=SIDE_EFFECTS)
    @mock.patch("modules.StateHandler.StateHandler.fill_json_fields")
    @mock.patch("urllib.request.urlopen",
                return_value=HTTPResponse(sock=socket.socket()))
    @mock.patch("http.client.HTTPResponse.read", return_value=ROBOTS_TXT)
    def test_main_logic(self, mock_1, mock_2, mock_3, mock_4):
        self.crawler.run()
        result = []
        self.show_folder(FOLDER, result)
        shutil.rmtree(FOLDER)
        self.assertSetEqual(set(result), set(FOLDER_DATA))

    def create_side_effects(self):
        SIDE_EFFECTS.append(
            self.get_reply_text("index.html", URL + "/index.html", "text/html",
                                1024, "utf-8"))
        SIDE_EFFECTS.append(
            self.get_reply_text("styles/style.css", URL + "/styles/style.css",
                                "text/html",
                                1024, "utf-8"))
        SIDE_EFFECTS.append(
            self.get_reply_text("main_page.html", URL + "/main_page.html",
                                "text/html", 1500, "utf-8"))
        SIDE_EFFECTS.append(self.get_reply_asset("image/shopping.jpg",
                                                 URL + "/image/shopping.jpg",
                                                 "image/jpg", 800, "utf-8"))
        SIDE_EFFECTS.append(
            self.get_reply_asset("image/food.png", URL + "/image/food.png",
                                 "image/png", 1100, "utf-8"))
        SIDE_EFFECTS.append(self.get_reply_asset("image/mountain.png",
                                                 URL + "/image/mountain.png",
                                                 "image/png", 690, "utf-8"))
        SIDE_EFFECTS.append(
            self.get_reply_asset("pics/allow/compass.png", URL +
                                 "/pics/allow/compass.png",
                                 "image/png", 880, "utf-8"))

    @staticmethod
    def get_reply_text(filename, url, type_str, content_len, encoding):
        with open(os.path.join(PATH, filename), 'r') as data:
            tmp_dict = {"url": url, "code": 200, "type": type_str,
                        "headers": {'Content-Length': content_len},
                        "content": bytes(data.read().encode(encoding)),
                        "encoding": encoding}
            return tmp_dict

    @staticmethod
    def get_reply_asset(filename, url, type_str, content_len, encoding):
        with open(os.path.join(PATH, filename), 'r') as data:
            tmp_dict = {"url": url, "code": 200, "type": type_str,
                        "headers": {'Content-Length': content_len},
                        "content": data.buffer.read(), "encoding": encoding}
            return tmp_dict

    def show_folder(self, folder, result):
        for path in os.listdir(folder):
            abs_path = os.path.join(folder, path)
            if os.path.isdir(abs_path):
                self.show_folder(abs_path, result)
            else:
                result.append(abs_path)
