#!/usr/bin/python
import json
import config
from aliyunsdkcore.client import AcsClient
from aliyunsdkemr.request.v20160408 import ResizeClusterV2Request


def query(cluster_id, host_groups):
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    clt = AcsClient(access_key_id, access_key_secret, region_id)  # set acessId and accessKey
    request = ResizeClusterV2Request.ResizeClusterV2Request()
    request.set_ClusterId(cluster_id)
    request.set_HostGroups(host_groups)

    response = clt.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))
    print(result)


cluster_id = 'C-C0B7882E41C1936E'

host_groups = [{
    'HostGroupName': 'GatewayGroup',
    'HostGroupType': 'GATEWAY',
    'ChargeType': 'Prepaid',
    'Period': 1,
    'NodeCount': 2,
    'InstanceType': 'ecs.g5.xlarge',
    'AutoRenew': True,
    'HostKeyPairName': '',
    'SysDiskCapacity': 300,
    'SysDiskType': 'CLOUD_SSD',
    'ClusterId': 'C-C0B7882E41C1936E',
}]

query(cluster_id, host_groups)
