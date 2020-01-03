

from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    # result = vpc_cli.describe_vpcs()
    # print(result)
    data = {
        'InstanceIds': ['cdbro-bguifh0g', 'cdb-0b8i9upw'],
        # 'Filters': [{'Name': 'zone', 'Values': ['ap-beijing-1']}]
    }
    result = cli.describe_instances(data)
    # result = vpc_cli.describe_db_zone_config(data)
    print(result['Items'][0])
    print(result['Items'][1])
