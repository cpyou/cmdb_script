from conf import tencent as tencent_conf
from tencent.base.cvm import TencentCvmSDKBase
import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('/Users/chenpuyu/Desktop/asset_data.xlsx')
    instance_ids = list(df.instance_id.values)
    cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    start = 0
    size = 100
    total = len(instance_ids)
    instances = []

    fail_ids = []
    while start < total:
        result = cli.describe_instances({'InstanceIds': instance_ids[start:start + size], 'Limit': size})
        terminate_ids = [instance['InstanceId'] for instance in result['InstanceSet']
                         if instance['InstanceState'] == 'STOPPED']
        # result = cli.stop_instances({'InstanceIds': instance_ids[start:start + 100]})
        start += size
        print(len(terminate_ids))
        for terminate_id in terminate_ids:
            print(terminate_id)
            try:
                result = cli.terminate_instances([terminate_id])
            except Exception as e:
                print(e)
                fail_ids.append(terminate_id)
    print('退还失败', fail_ids)

