

from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    data = {
        'InstanceId': 'cdb-bx27a3lu',
        # 'Filters': [{'Name': 'zone', 'Values': ['ap-beijing-1']}]
    }
    result = cli.describe_accounts(data)
    print(result)
    print([db_account['User'] for db_account in result['Items']])
