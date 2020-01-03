from tencent.base.cvm import TencentCvmSDKBase
from conf import tencent as tencent_conf

if __name__ == '__main__':
    cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    image_id = 'img-38nr8h15'
    key_ids = []
    instance_ids = []
    items = cli.describe_instances({'InstanceIds': instance_ids, 'Limit': 100})['InstanceSet']
    print(len(items))
    for item in items:
        params = {
            'InstanceId': item['InstanceId'],
            'HostName': item['InstanceName'],
            'ImageId': image_id,
            'LoginSettings': {'KeepImageLogin': True},
        }
        result = cli.reset_instance(params)
        print(result)
