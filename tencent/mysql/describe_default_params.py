

from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    vpc_cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    data = {
        'EngineVersion': '5.7'
    }
    result = vpc_cli.describe_default_params(data)
    print(result)
