import pandas as pd

from tencent.base.cvm import TencentCvmSDKBase
from conf import tencent as tencent_conf


class CVMInit(object):

    def __init__(self):
        self.cvm_cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)

    def run(self, filename):
        result = self.read_xlsx(filename)
        for item in result:
            result = self.create_cvm(item)
            print(result['InstanceIdSet'][0])

    @staticmethod
    def read_xlsx(filename):
        df = pd.read_excel(filename)
        df = df.where(df.notnull(), None)
        data = []
        for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
            # 根据i来获取每一行指定的数据 并利用to_dict转成字典
            row_data = df.ix[i, ['instance_type', 'hostname', 'disaster_recover_group_name']].to_dict()
            data.append(row_data)
        return data

    def get_disaster_recover_group_ids(self, group_name):
        if not group_name:
            return []
        data = {
            'Name': group_name
        }
        result = self.cvm_cli.describe_disaster_recover_groups(data)
        return [item['DisasterRecoverGroupId'] for item in result['DisasterRecoverGroupSet']]

    def create_cvm(self, data):
        """

        :param data: {
            "instance_type": "",
            "instance_name": "",
            "hostname": "",
            "disaster_recover_group_name": "",
            "disk_category": "",
            "disk_size": "",
            "disk_amount": "",
        }
        :return:
        """
        instance_type = data['instance_type']
        instance_name = data['instance_name']
        hostname = instance_name
        disaster_recover_group_name = data['disaster_recover_group_name']
        disaster_recover_group_ids = self.get_disaster_recover_group_ids(disaster_recover_group_name)

        zone = 'ap-beijing-5'
        image_id = 'img-38nr8h15'
        # key_ids = ["skey-jkn88g51"]
        security_group_ids = ["sg-fppqq00v"]
        vpc_id = 'vpc-j24hxiy4'
        # subnet_id = 'subnet-bwyknzbv'
        subnet_id = 'subnet-k1feuaxr'
        max_bandwidth = 500
        params = {
            'Placement': {'Zone': zone},
            'ImageId': image_id,
            'InstanceChargeType': 'PREPAID',
            'InstanceChargePrepaid': {'Period': 1, 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW'},
            'InstanceType': instance_type,
            'SystemDisk': {
                'DiskType': 'CLOUD_PREMIUM',
                'DiskSize': 100,  # 系统盘默认100G
            },
            # 'LoginSettings': {'KeyIds': key_ids},
            'VirtualPrivateCloud': {
                'VpcId': vpc_id,
                'SubnetId': subnet_id,
            },
            'SecurityGroupIds': security_group_ids,
            'InternetAccessible': {
                'InternetChargeType': 'TRAFFIC_POSTPAID_BY_HOUR',
                'InternetMaxBandwidthOut': max_bandwidth,
                'PublicIpAssigned': False,
            },
            'DisasterRecoverGroupIds': disaster_recover_group_ids,
            "InstanceName": instance_name,
            "HostName": hostname,
            "DataDisks": [],
        }
        # 'I3', 'D2' 不挂盘
        if instance_type.split('.')[0] not in ['I3', 'D2']:
            disk_size = 500
            disk_category = 'CLOUD_PREMIUM'
            disk_amount = 1
            for i in range(disk_amount):
                params['DataDisks'].append({'DiskType': disk_category, 'DiskSize': disk_size})

        result = self.cvm_cli.run_instances(params)
        return result


if __name__ == '__main__':
    cvm_init = CVMInit()
    # cvm_init.run('/Users/chenpuyu/Desktop/hadoop_0606.xlsx')
