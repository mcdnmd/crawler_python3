import requests


class Request:
    def send_request(self, page):
        url = f'https://{page}'
        with requests.Session() as s:
            try:
                response = s.get(url)
                return response
            except requests.exceptions.SSLError:
                try:
                    url = f'http://{page}'
                    return s.get(url)
                except requests.exceptions.RequestException:
                    return None
            except requests.exceptions.RequestException:
                return None
