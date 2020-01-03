import datetime
import json
import pandas as pd
from pprint import pprint
# from tencent.base.cvm import TencentCvmSDKBase
import requests

from aliyun.base.ecs import AliyunECS
from aliyun.base.ess import AliyunESS
from conf import aliyun_conf

INSTANCE_TYPE_GROUPS = {
    "1C1G": [],
    "1C2G": [],
    "2C4G": ["ecs.c5.large", "ecs.sn1ne.large", "ecs.sn1.medium", "ecs.n4.large"],
    "2C8G": [],
    "4C4G": ["ecs.ic5.xlarge"],
    "4C8G": ["ecs.c5.xlarge", "ecs.sn1ne.xlarge", "ecs.sn1.large", "ecs.n4.xlarge"],
    "4C16G": ["ecs.g5.xlarge", "ecs.sn2ne.xlarge", "ecs.sn2.large"]
}

DOMAIN = ''
TOKEN = ''


class ESSInit(object):

    def __init__(self, filename):
        self.filename = filename
        self.ess_cli = AliyunESS(
            aliyun_conf.AccessKeyID,
            aliyun_conf.AccessKeySecret,
            aliyun_conf.region_id)
        self.ecs_cli = AliyunECS(
            aliyun_conf.AccessKeyID,
            aliyun_conf.AccessKeySecret,
            aliyun_conf.region_id)
        self.excel_data = self.read_xlsx()
        token = TOKEN
        self.headers = {
            'ACCESS-TOKEN': '{}'.format(token)
        }
        self.unique_service = self.get_unique_service()
        self.service_dict = self.get_service_dict()

    def run(self):
        # pprint(self.excel_data)
        # pprint(self.get_service_slb())
        self.create_scaling()
        # self.bind_service()
        return

    def read_xlsx(self):
        df = pd.read_excel(self.filename)
        df = df.where(df.notnull(), None)
        data = []
        for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
            # 根据i来获取每一行指定的数据 并利用to_dict转成字典
            row_data = df.ix[i, ['host', 'ip', 'config', 'server', 'slb', 'slb_id', 'ecs_id', 'instance_type']].to_dict()
            data.append(row_data)
        return data

    def get_service_dict(self):
        service_dict = {}
        service_get_params = {
            'name__in': json.dumps(list(self.unique_service.keys())),
        }
        get_result = requests.get(
            f'{DOMAIN}/api/v1/cmdb/service/', params=service_get_params, headers=self.headers).json()
        for item in get_result['data']:
            service_dict[item['name']] = item['id']
        return service_dict

    def bind_service(self):
        ecs_ids = [item['ecs_id'] for item in self.excel_data]
        get_params = {
            'instance_id__in': json.dumps(ecs_ids),
        }
        get_result = requests.get(
            f'{DOMAIN}/api/v1/cmdb/host/', params=get_params, headers=self.headers).json()
        ecs_dict = {}
        for host in get_result['data']:
            ecs_dict[host['instance_id']] = host['id']

        service_dict = self.get_service_dict()
        print(service_dict)
        for item in self.excel_data:
            if not item['server']:
                continue
            service = item.get('server')
            if not service:
                continue
            host_id = ecs_dict[item['ecs_id']]
            service_id = service_dict.get(service)
            if not service_id:
                continue
            patch_params = {
                'env': 'qa',
                'services': [service_id],
            }
            print(host_id, patch_params)
            url = f'{DOMAIN}/api/v1/cmdb/host/{host_id}/'
            patch_result = requests.patch(url, json=patch_params, headers=self.headers).json()
            print(patch_result)

    def get_unique_service(self):
        service_slb_dict = {}
        for item in self.excel_data:
            if not item['server']:
                continue
            if not service_slb_dict.get(item['server']):
                service_slb_dict[item['server']] = {}
            if item['slb_id']:
                service_slb_dict[item['server']]['slb_id'] = item['slb_id'].strip()
            if item['ecs_id']:
                service_slb_dict[item['server']]['ecs_id'] = item['ecs_id'].strip()
            if item['instance_type']:
                service_slb_dict[item['server']]['instance_type'] = item['instance_type'].strip()
        print(service_slb_dict)
        return service_slb_dict

    def create_scaling(self):
        unique_service = self.get_unique_service()
        for service, params in unique_service.items():
            if not service:
                continue
            service_id = self.service_dict.get(service)
            if not service_id:
                continue
            print(service, params)
            slb_id = params.get('slb_id', False)
            scaling_group_id, salcing_group_id_ = self.create_scaling_group(service, slb_id)
            instance_type = params['instance_type']
            image_id = 'm-bp135nlsftzn7ikblmdo'
            scaling_configuration_id = self.create_scaling_configuration(
                service, scaling_group_id, salcing_group_id_, image_id, instance_type)
            enable_params = {
                'scaling_group_id': scaling_group_id,
                'active_scaling_configuration_id': scaling_configuration_id,
            }
            self.ess_cli.enable_scaling_group(enable_params)
            self.create_rule(scaling_group_id)
            print(service, image_id, scaling_group_id, scaling_configuration_id)

    def create_images(self, service, instance_id):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        image_name = f'ess_image_perf_{service}_{current_time}'
        create_result = self.ecs_cli.create_image(instance_id, image_name)
        print(create_result)
        return create_result['ImageId']

    def create_scaling_group(self, service, slb_id=False):
        apply_params = {
            'scaling_group_name': f'asc_ali_perf_{service}',
            'v_switch_ids': ['vsw-bp1e4o3b7p5d7xholxr0a'],
            'max_size': 200,
            'min_size': 0,
        }
        if slb_id:
            apply_params['load_balancer_ids'] = [slb_id]
        create_result = self.ess_cli.create_scaling_group(apply_params)
        salcing_group_id = create_result['ScalingGroupId']
        create_data = dict(
            scaling_group_name=apply_params['scaling_group_name'],
            scaling_group_id=salcing_group_id,
            provider=1,
            service=self.service_dict[service],
            region=1,
            env='qa',
            max_size=apply_params['max_size'],
            min_size=apply_params['min_size'],
            switch_ids=apply_params['v_switch_ids'],
            status='Pending',
            properties={}
        )
        req_result = requests.post(
            f'{DOMAIN}/api/v1/cmdb/scaling-group/', json=create_data, headers=self.headers).json()
        salcing_group_id_ = req_result['data']['id']
        return salcing_group_id, salcing_group_id_

    def create_scaling_configuration(self, service, scaling_group_id, salcing_group_id_, image_id, instance_type):
        scaling_configuration_name = f'asc_{service}'
        apply_params = {
            'scaling_group_id': scaling_group_id,
            'scaling_configuration_name': scaling_configuration_name,
            'instance_types': [instance_type],
            'security_group_ids': ['sg-bp10nbdyhr7t7colnm2f'],
            'image_id': image_id,
            'system_disk_category': 'cloud_efficiency',
            'system_disk_size': 40,
            # bash脚本，将hostname解析写入/etc/hosts
            # #!/bin/bash
            # grep -R $(hostname) /etc/hosts || echo "127.0.0.1 $(hostname)" >> /etc/hosts
            'user_data': 'IyEvYmluL2Jhc2gKZ3JlcCAtUiAkKGhvc3RuYW1lKSAvZXRjL2hvc3RzIHx8IGVjaG8gIjEyNy4wLjAuMSAkKGhvc3RuYW1lKSIgPj4gL2V0Yy9ob3N0cw',
        }
        scaling_configuration_id = self.ess_cli.create_scaling_configuration(apply_params)['ScalingConfigurationId']
        create_params = {
            'scaling_configuration_id': scaling_configuration_id,
            'scaling_configuration_name': scaling_configuration_name,
            'image_id': image_id,
            'instance_types': apply_params['instance_types'],
            'system_disk_size': apply_params['system_disk_size'],
            'system_disk_category': apply_params['system_disk_category'],
            'security_group_ids': ['sg-bp10nbdyhr7t7colnm2f'],
            'scaling_group': salcing_group_id_,
        }
        req_result = requests.post(
            f'{DOMAIN}/api/v1/cmdb/scaling-configuration/',
            json=create_params, headers=self.headers).json()
        return scaling_configuration_id

    def create_rule(self, scaling_group_id):
        apply_params = {
            'scaling_group_id': scaling_group_id,
            'scaling_rule_name': "cmdb_scaling_rule",
            'cooldown': 300,
            'scaling_rule_type': 'SimpleScalingRule',
            'adjustment_type': 'QuantityChangeInCapacity',
            'adjustment_value': 10,
        }
        return self.ess_cli.create_scaling_rule(apply_params)


if __name__ == '__main__':
    filename = '/Users/chenpuyu/Desktop/PERF压测环境服务分布2.xlsx'
    cvm_init = ESSInit(filename)
    cvm_init.run()
