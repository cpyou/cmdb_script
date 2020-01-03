# -*- coding: utf8 -*-
#
import hashlib
import json
import os

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.cdb.v20170320 import models, cdb_client


class TencentMysqlSDKBase(object):

    def __init__(self, secret_id, secret_key, region):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        cred = credential.Credential(secret_id, secret_key)
        self.client = cdb_client.CdbClient(cred, region)

    def create_instances(self, data=None):
        req = models.CreateDBInstanceRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.CreateDBInstance(req)
        return json.loads(resp.to_json_string())

    def describe_instances(self, data=None):
        req = models.DescribeDBInstancesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeDBInstances(req)
        return json.loads(resp.to_json_string())

    def describe_db_zone_config(self, data=None):
        req = models.DescribeDBZoneConfigRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeDBZoneConfig(req)
        return json.loads(resp.to_json_string())

    def init_db_instances(self, data=None):
        req = models.InitDBInstancesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.InitDBInstances(req)
        return json.loads(resp.to_json_string())

    def describe_default_params(self, data=None):
        req = models.DescribeDefaultParamsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeDefaultParams(req)
        return json.loads(resp.to_json_string())

    def create_accounts(self, data=None):
        req = models.CreateAccountsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.CreateAccounts(req)
        return json.loads(resp.to_json_string())

    def describe_accounts(self, data=None):
        req = models.DescribeAccountsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeAccounts(req)
        return json.loads(resp.to_json_string())

    def modify_account_privileges(self, data=None):
        req = models.ModifyAccountPrivilegesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.ModifyAccountPrivileges(req)
        return json.loads(resp.to_json_string())
