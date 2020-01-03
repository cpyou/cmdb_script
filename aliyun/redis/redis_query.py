# 查询所有实例
import json
from conf import aliyun_conf


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_PageNumber(data.get('page', 1))
    request.set_PageSize(data.get('size', 50))
    if data.get('instance_ids'):
        request.set_InstanceIds(','.join(data['instance_ids']))

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result


def main():
    params1 = {
        'instance_ids': ['r-2zezljietelpboa8nh']
    }

    result = query(params1)
    print(result['Instances']['KVStoreInstance'][0])


if __name__ == '__main__':
    main()
