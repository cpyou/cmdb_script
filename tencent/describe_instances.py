from conf import tencent as tencent_conf
from tencent.base.cvm import TencentCvmSDKBase

if __name__ == '__main__':
    cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    instance_ids = [
        'ins-nkznp8dd',
    ]
    items = cli.describe_instances({'InstanceIds': instance_ids, 'Limit': 100})['InstanceSet']
    # for item in items:
    #     print(item['PrivateIpAddresses'][0], item['InstanceName'])
    for item in sorted([(item['InstanceName'], item['InstanceId'], item['PrivateIpAddresses'][0],) for item in items]):
        print(item[0], item[2])
    print([item['PrivateIpAddresses'][0] for item in items])
    print(len(set([item['PrivateIpAddresses'][0] for item in items])))
