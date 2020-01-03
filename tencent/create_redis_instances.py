from conf import tencent as tencent_conf
from tencent.base.redis import TencentRedisSDKBase

if __name__ == '__main__':
    cli = TencentRedisSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    # 测试环境
    # data = {
    #     # 'ZoneId': 'ap-beijing-4',
    #     'ZoneId': 800004,
    #     'TypeId': 7,
    #     'MemSize': 12 * 1024,
    #     'VpcId': 'vpc-8qmpjk6e',
    #     'SubnetId': 'subnet-esc2kgyj',
    #     'Password': '',
    #     'BillingMode': 1,
    #     'Period': 1,
    #     'AutoRenew': 1,
    #     'GoodsNum': 1,
    #     'RedisShardNum': 3,
    #     'RedisReplicasNum': 1,
    #     'InstanceName': 'cpytest-测试申请redis-陈普雨'
    # }

    data = {
        'ZoneId': 800005,
        'TypeId': 7,
        'MemSize': 12 * 1024,
        'VpcId': 'vpc-j24hxiy4',
        'SubnetId': 'subnet-66yhtd3x',
        'Password': '',
        'BillingMode': 1,
        'Period': 1,
        'AutoRenew': 1,
        'GoodsNum': 1,
        'RedisShardNum': 3,
        'RedisReplicasNum': 1,
        'InstanceName': 'cpytest-测试申请redis-陈普雨'
    }
    result = cli.create_instances(data)
    print(result)
