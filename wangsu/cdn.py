import datetime
from hashlib import sha256
import hmac
import base64
import requests

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


class WangsuCDN:
    def __init__(self, username, apikey):
        self.username = username
        self.apikey = apikey
        self.http_host = 'https://open.chinanetcenter.com'

    @staticmethod
    def get_date():
        date_gmt = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        return date_gmt

    @staticmethod
    def get_auth(username, apikey, date):
        signed_apikey = hmac.new(apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
        signed_apikey = base64.b64encode(signed_apikey)
        signed_apikey = username + ":" + signed_apikey.decode()
        signed_apikey = base64.b64encode(signed_apikey.encode('utf-8'))
        return signed_apikey

    def create_header(self, accept='application/json'):
        date = self.get_date()
        auth_str = self.get_auth(self.username, self.apikey, date)
        headers = {
            'Date': date,
            'Accept': accept,
            'Content-type': accept,
            'Authorization': 'Basic ' + auth_str.decode()
        }
        return headers

    def get_data(self, url, params=None):
        headers = self.create_header()
        return requests.get(url, headers=headers, params=params)

    def post_data(self, url, data, params=None):
        headers = self.create_header()
        return requests.post(url, headers=headers, json=data, params=params)

    @staticmethod
    def print_resp(resp):
        headers_post = dict(resp.headers)
        tmp_str = "statusCode:{}\nDate:{}\nContent-Length:{}\nConnection:{}\nx-cnc-request-id:{}\n\n{}".format(
            resp.status_code,
            headers_post.get('Date'),
            headers_post.get('Content-Length'),
            headers_post.get('Connection'),
            headers_post.get('x-cnc-request-id'),
            resp.text)
        print(tmp_str)

    def refresh_urls(self, urls: list):
        """

        :param urls:
        :return:
        """
        url = f'{self.http_host}/ccm/purge/ItemIdReceiver'
        params = {
            'urls': urls,
        }
        return self.post_data(url, params).json()

    def refresh_dirs(self, dirs: list):
        """

        :param dirs:
        :return:
        """
        url = f'{self.http_host}/ccm/purge/ItemIdReceiver'
        data = {
            'dirs': dirs,
        }
        return self.post_data(url, data).json()

    def prefetch_urls(self, urls: list):
        """

        :param urls:
        :return:
        """
        url = f'{self.http_host}/ccm/fetch/ItemIdReceiver'
        data = {
            "fetchOption": "Y",
            'urls': urls,
            "isRange": 0
        }
        return self.post_data(url, data).json()

    def get_all_domain(self):
        url = f'{self.http_host}/api/domain'
        return self.get_data(url).json()


if __name__ == '__main__':
    from conf import wangsu

    cdn = WangsuCDN(wangsu.secret_id, wangsu.secret_key)
    # result = cdn.refresh_urls(['http://img0.test.com/PXQ/assets/img/2376kdBhPM_.jpeg'])
    # result = cdn.prefetch_urls(['http://img0.test.com/assets/app/img/WechatIMG58.jpeg'])
    result = cdn.get_all_domain()
    # cdn.print_resp(result)
    print(result)
