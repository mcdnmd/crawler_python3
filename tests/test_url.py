import unittest
from modules.Url import Url


class UrlTest(unittest.TestCase):
    def test_simple_url(self):
        URL = 'https://anytask.org'
        url = Url(URL)
        self.assertEqual(url.filename, 'index.html')

    def test_img_url(self):
        URL = 'https://s3.tproger.ru/uploads/2020/07/xsolla-50x50.png'
        url = Url(URL)
        self.assertEqual(url.filename, 'xsolla-50x50.png')

    def test_complex_url(self):
        URL = 'https://tproger.ru/translations/regular-expression-python/'
        url = Url(URL)
        self.assertEqual(url.dirname,
                         '/translations/regular-expression-python')
