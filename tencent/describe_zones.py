from conf import tencent as tencent_conf
from tencent.base.redis import TencentRedisSDKBase

if __name__ == '__main__':
    vpc_cli = TencentRedisSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    result = vpc_cli.describe_redis_zones()
    # print(result['RegionSet'])
    for item in result['RegionSet']:
        print(item)
        print()

