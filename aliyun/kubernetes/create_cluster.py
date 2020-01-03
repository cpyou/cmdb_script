# from aliyun.base.kubernetes import KubernetesSDK
from conf import aliyun_conf
import json

from aliyunsdkcore.client import AcsClient


class KubernetesSDK(object):

    def __init__(self, region_id, access_key_id, access_key_secret):
        self.AccessKeyID = access_key_id
        self.AccessKeySecret = access_key_secret
        self.region_id = region_id
        self.client = AcsClient(self.AccessKeyID, self.AccessKeySecret, self.region_id, timeout=35)

    def create_cluster(self, data=None):
        from aliyunsdkcs.request.v20151215 import CreateClusterRequest
        request = CreateClusterRequest.CreateClusterRequest()
        request.add_header('Content-Type', 'application/json')
        # request.set_accept_format('json')
        request.set_content(json.dumps(data).encode('UTF-8'))
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result


k8s_cli = KubernetesSDK(access_key_id=aliyun_conf.AccessKeyID,
                        access_key_secret=aliyun_conf.AccessKeySecret,
                        region_id=aliyun_conf.region_id)
body = {
    "cluster_type": "Kubernetes",
    "name": "cpy-test-Kubernetes-cluster",
    "region_id": "cn-beijing",
    "disable_rollback": True,
    "timeout_mins": 60,
    "kubernetes_version": "1.12.6-aliyun.1",
    "snat_entry": False,
    "public_slb": False,
    "cloud_monitor_flags": True,
    "node_cidr_mask": "25",
    "proxy_mode": "ipvs",
    "tags": [],
    "addons": [
        {
            "name": "terway"
        }
    ],
    "key_pair": "",
    "master_count": 3,
    "master_vswitch_ids": [
        "vsw-2ze2g8lynduicxtp0sz0h",
        "vsw-2ze2g8lynduicxtp0sz0h",
        "vsw-2ze2g8lynduicxtp0sz0h"
    ],
    "master_instance_types": [
        "ecs.c5.xlarge",
        "ecs.c5.xlarge",
        "ecs.c5.xlarge"
    ],
    "master_system_disk_category": "cloud_efficiency",
    "master_system_disk_size": 100,

    "worker_instance_types": [
        "ecs.c5.xlarge"
    ],
    "num_of_nodes": 1,
    "worker_system_disk_category": "cloud_efficiency",
    "worker_system_disk_size": 100,
    "vpcid": "vpc-2zeh81ixmvuusbihybhsb",
    "container_cidr": "10.90.0.0/17",
    "service_cidr": "10.85.0.0/17",

    # 包年包月（按量付费以下参数不传）
    "master_instance_charge_type": "PrePaid",
    "worker_instance_charge_type": "PrePaid",
    "master_period": 1,
    "worker_period": 1,
    "master_period_unit": "Month",
    "worker_period_unit": "Month",
    "master_auto_renew": True,
    "master_auto_renew_period": 1,
    "worker_auto_renew": True,
    "worker_auto_renew_period": 1,

    #
    "worker_data_disk": True,
    "worker_data_disk_category": "cloud_efficiency",
    "worker_data_disk_size": 100,
}
# result = k8s_cli.create_cluster(data=body)
# print(result)
