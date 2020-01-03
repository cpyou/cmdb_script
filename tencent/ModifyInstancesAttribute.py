from conf import tencent as tencent_conf
from tencent.base.cvm import TencentCvmSDKBase

if __name__ == '__main__':
    cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    # result = vpc_cli.describe_vpcs()
    # print(result)
    # data = {
    #     # 'Filters': [{'Name': 'zone', 'Values': ['ap-beijing-1']}]
    # }
    #
    # result = cli.describe_instances(data)
    # print(result['InstanceSet'][0])
    instance_ids = []

    items = cli.describe_instances({'InstanceIds': instance_ids, 'Limit': 100})['InstanceSet']
    # for item in items:
    #     print(item['PrivateIpAddresses'][0], item['InstanceName'])
    for item in sorted([(item['InstanceName'], item['InstanceId'], item['PrivateIpAddresses'][0],) for item in items]):
        midify_data = {
            'InstanceIds': [item[1]],
            'InstanceName': item[0][:len(item[0]) - 18],
        }
        cli.modify_instances_attribute(midify_data)
        print(item[0], item[2])
    print([item['PrivateIpAddresses'][0] for item in items])
    print(len(set([item['PrivateIpAddresses'][0] for item in items])))
