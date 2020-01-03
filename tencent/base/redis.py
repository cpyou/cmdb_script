# -*- coding: utf8 -*-
#
import hashlib
import json
import os

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.redis.v20180412 import redis_client, models


class TencentRedisSDKBase(object):

    def __init__(self, secret_id, secret_key, region):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        cred = credential.Credential(secret_id, secret_key)
        self.client = redis_client.RedisClient(cred, region)

    def describe_instances(self, data=None):
        req = models.DescribeInstancesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeInstances(req)
        return json.loads(resp.to_json_string())

    def create_instances(self, data=None):
        """"
        https://cloud.tencent.com/document/api/239/20026
        """
        req = models.CreateInstancesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.CreateInstances(req)
        return json.loads(resp.to_json_string())

    def describe_redis_zones(self, data=None):
        """"
        https://cloud.tencent.com/document/api/239/20026
        """
        req = models.DescribeProductInfoRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeProductInfo(req)
        return json.loads(resp.to_json_string())

