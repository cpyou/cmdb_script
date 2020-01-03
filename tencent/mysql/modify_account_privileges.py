from conf import tencent as tencent_conf
from tencent.base.mysql import TencentMysqlSDKBase

if __name__ == '__main__':
    cli = TencentMysqlSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    data = {
        'InstanceId': 'cdb-bx27a3lu',
        'Accounts': [
            {'User': 'cpy_test_account', 'Host': '%'},
        ],
        'GlobalPrivileges': ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "REFERENCES", "INDEX", "ALTER",
                             "SHOW DATABASES", "CREATE TEMPORARY TABLES", "LOCK TABLES", "EXECUTE", "CREATE VIEW",
                             "SHOW VIEW", "CREATE ROUTINE", "ALTER ROUTINE", "EVENT", "TRIGGER"]
    }
    result = cli.modify_account_privileges(data)
    print(result)
