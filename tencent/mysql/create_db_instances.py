from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    # 测试
    # data = {
    #     'Memory': 1000,
    #     'Volume': 25,
    #     'Period': 1,
    #     'GoodsNum': 1,
    #     'Zone': 'ap-beijing-5',
    #     'UniqVpcId': 'vpc-ksofzvl2',
    #     'UniqSubnetId': 'subnet-paksquql',
    #     'InstanceRole': 'master',
    #     'EngineVersion': '5.7',
    #     'ProtectMode': 0,
    #     'AutoRenewFlag': 1,
    #     'InstanceName': 'cpytest-测试申请mysq-陈普雨',
    #     #
    #     'Password': '',
    #     'ParamList': [
    #         {'Name': 'character_set_server', 'Value': 'utf8mb4'},
    #         {'Name': 'lower_case_table_names', 'Value': 1},
    #     ],
    # }

    # 生产
    data = {
        'Memory': 1000,
        'Volume': 25,
        'Period': 1,
        'GoodsNum': 1,
        'Zone': 'ap-beijing-5',
        'SecurityGroup': ["sg-4b9q4ggp"],
        'UniqVpcId': 'vpc-j24hxiy4',
        'UniqSubnetId': 'subnet-66yhtd3x',
        'InstanceRole': 'master',
        'EngineVersion': '5.7',
        'ProtectMode': 0,
        'AutoRenewFlag': 1,
        'InstanceName': 'cpytest-测试申请mysq-陈普雨',
        #
        'Password': '',
        'ParamList': [
            {'Name': 'character_set_server', 'Value': 'utf8mb4'},
            {'Name': 'lower_case_table_names', 'Value': 1},
        ],
    }
    result = cli.create_instances(data)
    print(result)
