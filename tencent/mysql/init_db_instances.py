

from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    vpc_cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    data = {
        'InstanceIds': ['cdb-pmdtsjla'],
        'NewPassword': '',
        'Parameters': [
            {'Name': 'character_set_server', 'Value': 'utf8mb4'},
            {'Name': 'lower_case_table_names', 'Value': 1},
        ],
    }
    result = vpc_cli.init_db_instances(data)
    print(result['Items'][0])
