from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)

    # 生产
    data = {
        'InstanceId': '',
        'Accounts': [
            {'User': 'cpy_test_account', 'Host': '%'},
            {'User': 'dms', 'Host': '%'},
        ],
        'Password': '',
    }
    result = cli.create_accounts(data)
    print(result)
