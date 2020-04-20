import unittest
from aliyun.base.waf import AliyunWAF
from conf import aliyun_conf


class TestWAF(unittest.TestCase):
    """
    测试WAF
    """

    def setUp(self):
        self.cli = AliyunWAF(aliyun_conf.AccessKeyID, aliyun_conf.AccessKeySecret, aliyun_conf.region_id)
        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def test_describe_pay_info(self):
        res = self.cli.describe_pay_info()
        self.assertTrue(isinstance(res, dict))
        print(res)

    def test_describe_domain_names(self):
        res = self.cli.describe_domain_names()
        print(res)

    def test_describe_domain_config(self):
        res = self.cli.describe_domain_names()
        domain = res['Result']['DomainNames'][0]
        res = self.cli.describe_domain_config(domain=domain)
        print(res)


if __name__ == '__main__':
    unittest.main()
