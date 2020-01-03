import json

from tencentcloud.common import credential
# 导入对应产品模块的client models。
from tencentcloud.vpc.v20170312 import vpc_client, models


class TencentVpcSDKBase(object):

    def __new__(cls, *args, **kwargs):
        print('new')

    def __init__(self, secret_id, secret_key, region):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        cred = credential.Credential(secret_id, secret_key)
        self.client = vpc_client.VpcClient(cred, region)

    def describe_vpcs(self, data=None):
        req = models.DescribeVpcsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeVpcs(req)
        return json.loads(resp.to_json_string())

    def describe_subnets(self, data=None):
        req = models.DescribeSubnetsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeSubnets(req)
        return json.loads(resp.to_json_string())
