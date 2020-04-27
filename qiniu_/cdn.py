import qiniu

from qiniu import http

from qiniu import CdnManager


class QiniuCdnManager(CdnManager):
    def __init__(self, auth):
        self.api_server = 'api.qiniu.com'
        super(QiniuCdnManager, self).__init__(auth)

    def __get(self, url, params=None):
        return http._get(url, params, self.auth)

    def get_all_domains(self, limit):
        """
        文档地址：https://developer.qiniu.com/fusion/api/4246/the-domain-name#9
        :param limit: 每页大小
        :return:  domain name list
        """
        url = 'http://{0}/domain'.format(self.api_server)
        params = {'limit': limit}
        domains = []
        while True:
            res = self.__get(url, params=params)
            domains.extend(res[0]['domains'])
            marker = res[0]['marker']
            if marker:
                params['marker'] = marker
            else:
                break
        return domains


class QiniuCDN:
    def __init__(self, access_key, secret_key):
        # 账户ak，sk
        self.auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
        self.cdn_manager = QiniuCdnManager(self.auth)

    def cdn_domains(self, limit=100):
        # 获取域名列表
        domains = self.cdn_manager.get_all_domains(limit)
        return [item['name'] for item in domains]


if __name__ == '__main__':
    from conf import qiniu
    cdn = QiniuCDN(qiniu.secret_id, qiniu.secret_key)
    cdn.cdn_domains(limit=1000)
