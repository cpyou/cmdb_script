

from conf import tencent as tencent_conf
from tencent.cvm import TencentCvmSDKBase

if __name__ == '__main__':
    cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    # result = vpc_cli.describe_vpcs()
    # print(result)
    data = {
        'Name': 'di-h1-rm-group',
        'Limit': 100,
    }
    result = cli.describe_disaster_recover_groups(data)
    # print([item['DisasterRecoverGroupId'] for item in result['DisasterRecoverGroupSet']])
    print(result['DisasterRecoverGroupSet'])
    # print(len(result['DisasterRecoverGroupSet']))
    # print(len(list(set([item['Name'] for item in result['DisasterRecoverGroupSet']]))))
    # for item in result['DisasterRecoverGroupSet']:
    #     print(item['DisasterRecoverGroupId'], item['Name'])
