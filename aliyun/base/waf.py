import json
import logging

from aliyun.base import AliyunSDKBase
from aliyunsdkcore.request import CommonRequest

logger = logging.getLogger('django')


class AliyunWAF(AliyunSDKBase):

    @staticmethod
    def get_common_request():
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('wafopenapi.cn-hangzhou.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2018-01-17')
        request.add_query_param('RegionId', "cn-hangzhou")
        return request

    def get_request(self):
        request = self.get_common_request()
        instance_id = self.describe_pay_info()['Result']['InstanceId']
        request.add_query_param('InstanceId', instance_id)
        return request

    def describe_pay_info(self):
        """
        调用DescribePayInfo接口获取指定地域的WAF实例当前信息。
        文档: https://help.aliyun.com/document_detail/86651.html?spm=a2c4g.11186623.6.695.187f7739Mfd6cW
        Args:

        Returns:

        """
        request = self.get_common_request()
        request.set_action_name('DescribePayInfo')
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def describe_domain_names(self):
        """
        调用DescribeDomainNames接口获取指定WAF实例中已添加的域名名称列表。
        文档: https://help.aliyun.com/document_detail/86373.html?spm=a2c4g.11186623.6.698.56b26f0469Z21R
        Args:

        Returns:

        """
        request = self.get_request()
        request.set_action_name('DescribeDomainNames')
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def describe_domain_config(self, domain):
        """
        调用DescribeDomainConfig接口获取指定域名的转发配置信息。
        文档: https://help.aliyun.com/document_detail/86389.html?spm=a2c4g.11186623.6.699.187f77398oBHNB
        Args:
            domain: 已添加的域名名称
        Returns:

        """
        request = self.get_request()
        request.set_action_name('DescribeDomainConfig')
        request.add_query_param('Domain', domain)
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def modify_domain_config_source_ips(self, domain, source_ips):
        """
        调用ModifyDomainConfig接口修改指定域名配置信息。
        文档: https://help.aliyun.com/document_detail/86448.html?spm=a2c4g.11186623.6.702.cef46f04eB832M
        Args:
            domain: 域名
            source_ips: 源站IPS
        Returns:

        """
        request = self.get_request()
        request.set_action_name('ModifyDomainConfig')
        request.add_query_param('domain', domain)
        request.add_query_param('IsAccessProduct', 0)
        request.add_query_param('Protocols', ['http', 'https'])
        request.add_query_param('SourceIps', source_ips)
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result
