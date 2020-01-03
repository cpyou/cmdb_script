import hashlib
import json
import os

from tencentcloud.common import credential
# 导入对应产品模块的client models。
from tencentcloud.cvm.v20170312 import cvm_client, models


class TencentCvmSDKBase(object):

    def __init__(self, secret_id, secret_key, region):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        cred = credential.Credential(secret_id, secret_key)
        self.client = cvm_client.CvmClient(cred, region)

    def describe_regions(self, data=None):
        req = models.DescribeRegionsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeRegions(req)
        return json.loads(resp.to_json_string())

    def describe_zones(self, data=None):
        req = models.DescribeZonesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeZones(req)
        return json.loads(resp.to_json_string())

    def describe_instances(self, data=None):
        req = models.DescribeInstancesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeInstances(req)
        return json.loads(resp.to_json_string())

    def run_instances(self, data):
        req = models.RunInstancesRequest()
        data['ClientToken'] = hashlib.sha1(os.urandom(64)).hexdigest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.RunInstances(req)
        return json.loads(resp.to_json_string())

    def stop_instances(self, data):
        req = models.StopInstancesRequest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.StopInstances(req)
        return json.loads(resp.to_json_string())

    def start_instances(self, data):
        req = models.StartInstancesRequest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.StartInstances(req)
        return json.loads(resp.to_json_string())

    def reset_instance(self, data):
        req = models.ResetInstanceRequest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.ResetInstance(req)
        return json.loads(resp.to_json_string())

    def describe_images(self, data=None):
        req = models.DescribeImagesRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeImages(req)
        return json.loads(resp.to_json_string())

    def describe_zone_instance_config_infos(self, data=None):
        req = models.DescribeZoneInstanceConfigInfosRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeZoneInstanceConfigInfos(req)
        return json.loads(resp.to_json_string())

    def describe_instance_type_configs(self, data=None):
        req = models.DescribeInstanceTypeConfigsRequest()
        if data:
            params = json.dumps(data)
            req.from_json_string(params)
        resp = self.client.DescribeInstanceTypeConfigs(req)
        return json.loads(resp.to_json_string())

    def terminate_instances(self, instance_ids=list):
        data = {
            'InstanceIds': instance_ids
        }
        req = models.TerminateInstancesRequest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.TerminateInstances(req)
        return json.loads(resp.to_json_string())

    def describe_disaster_recover_groups(self, data=None):
        req = models.DescribeDisasterRecoverGroupsRequest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.DescribeDisasterRecoverGroups(req)
        return json.loads(resp.to_json_string())

    def modify_instances_attribute(self, data=None):
        req = models.ModifyInstancesAttributeRequest()
        params = json.dumps(data)
        req.from_json_string(params)
        resp = self.client.ModifyInstancesAttribute(req)
        return json.loads(resp.to_json_string())
