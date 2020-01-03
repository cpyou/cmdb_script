

from conf import tencent as tencent_conf
from tencent.base.vpc import TencentVpcSDKBase

if __name__ == '__main__':
    vpc_cli = TencentVpcSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    data = {
        'SubnetIds': ['subnet-k1feuaxr']
    }
    result = vpc_cli.describe_subnets(data)
    print(result)

