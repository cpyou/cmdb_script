# -- coding: utf-8 --
import time
import random
import hmac
import base64
import copy
import urllib.request, urllib.parse, urllib.error
import http.client

import collections
import sys
from hashlib import sha1

import config


class V3Api:
    # 定义变量
    URI_PREFIX = '/v3/openapi/apps/'
    OS_PREFIX = 'OPENSEARCH'
    VERB = 'GET'

    def __init__(self, address='', port=''):
        self.address = address
        self.port = port

    def run_query(self, app_name=None, access_key=None, secret=None, http_header=None, http_params=None):
        if http_params is None:
            http_params = {}
        if http_header is None:
            http_header = {}
        query, header = self.build_query(
            app_name=app_name,
            access_key=access_key,
            secret=secret,
            http_header=http_header,
            http_params=http_params)

        conn = http.client.HTTPConnection(self.address, self.port)
        conn.request(self.VERB, url=query, headers=header)
        response = conn.getresponse()

        return response.status, response.getheaders(), response.read()

    def build_query(self,
                    app_name=None,
                    access_key=None,
                    secret=None,
                    http_header=None,
                    http_params=None):
        if http_params is None:
            http_params = {}
        if http_header is None:
            http_header = {}
        uri = self.URI_PREFIX
        if app_name is not None:
            uri += app_name

        param = []
        for key, value in http_params.items():
            param.append(urllib.parse.quote(key) + '=' + urllib.parse.quote(value))

        query = ('&'.join(param))

        request_header = self.build_request_header(uri=uri,
                                                   access_key=access_key,
                                                   secret=secret,
                                                   http_params=http_params,
                                                   http_header=http_header)

        return uri + query, request_header

    # 此处为签名代码实现
    def build_authorization(self, uri, access_key, secret, http_params, request_header):
        canonicalized = self.VERB + '\n' \
                        + self.__get_header(request_header, 'Content-MD5', '') + '\n' \
                        + self.__get_header(request_header, 'Content-Type', '') + '\n' \
                        + self.__get_header(request_header, 'Date', '') + '\n' \
                        + self.__canonicalized_headers(request_header) \
                        + self.__canonicalized_resource(uri, http_params)

        signature_hmac = hmac.new(secret.encode('utf-8'), canonicalized.encode('utf-8'), 'sha1')
        signature = base64.b64encode(signature_hmac.digest())

        return '%s %s%s%s' % (self.OS_PREFIX, access_key, ':', signature.decode('utf-8'))

    def __get_header(self, header, key, default_value=None):
        if key in header and header[key] is not None:
            return header[key]
        return default_value

    def __canonicalized_resource(self, uri, http_params):
        canonicalized = urllib.parse.quote(uri).replace('%2F', '/')

        sorted_params = sorted(list(http_params.items()), key=lambda http_params: http_params[0])
        params = []
        for (key, value) in sorted_params:
            if value is None or len(value) == 0:
                continue

            params.append(urllib.parse.quote(key) + '=' + urllib.parse.quote(value))

        return canonicalized + '&'.join(params)

    def generate_date(self, fmt="%Y-%m-%dT%H:%M:%SZ", timestamp=None):
        if timestamp is None:
            return time.strftime(fmt, time.gmtime())
        else:
            return time.strftime(fmt, timestamp)

    def generate_n_once(self):
        return str(int(time.time() * 100)) + str(random.randint(1000, 9999))

    def __canonicalized_headers(self, request_header):
        header = {}
        for key, value in request_header.items():
            if key is None or value is None:
                continue
            k = key.strip(' \t')
            v = value.strip(' \t')
            if k.startswith('X-Opensearch-') and len(v) > 0:
                header[k] = v

        if len(header) == 0:
            return ''

        sorted_header = sorted(list(header.items()), key=lambda header: header[0])
        canonicalized = ''
        for (key, value) in sorted_header:
            canonicalized += (key.lower() + ':' + value + '\n')

        return canonicalized

    # 构建Request Header
    def build_request_header(self, uri, access_key, secret, http_params, http_header):
        request_header = copy.deepcopy(http_header)
        if 'Content-MD5' not in request_header:
            request_header['Content-MD5'] = ''
        if 'Content-Type' not in request_header:
            request_header['Content-Type'] = 'application/json'
        if 'Date' not in request_header:
            request_header['Date'] = self.generate_date()
        if 'X-Opensearch-Nonce' not in request_header:
            request_header['X-Opensearch-Nonce'] = self.generate_n_once()
        if 'Authorization' not in request_header:
            request_header['Authorization'] = self.build_authorization(uri,
                                                                       access_key,
                                                                       secret,
                                                                       http_params,
                                                                       request_header)
        key_del = []
        for key, value in request_header.items():
            if value is None:
                key_del.append(key)

        for key in key_del:
            del request_header[key]

        return request_header


if __name__ == '__main__':
    accesskey_id = config.AccessKeyID
    accesskey_secret = config.AccessKeySecret
    # 下面host地址，替换为访问对应应用api地址，例如华东1区
    internet_host = 'opensearch-{}.aliyuncs.com'.format(config.region_id)
    appname = ''

    api = V3Api(address=internet_host, port='80')
    # 下面为设置查询信息
    query_subsentences = {
    }
    data = api.run_query(app_name=appname, access_key=accesskey_id, secret=accesskey_secret,
                         http_params=query_subsentences,
                         http_header={})
    print(data)
