# 查询所有实例
import json
import config
import re


def camel2underscore(jsondata):
    result = {}
    for (k, v) in jsondata.items():
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', k)
        k = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        result[k] = camel2underscore(v) if isinstance(v, dict) else v
    return result


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkdds.request.v20151201 import DescribeDBInstancesRequest
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()

    # 发起API请求并显示返回值
    # response = client.do_action(request)
    # return response
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))
    items = [camel2underscore(instance) for instance in result['DBInstances']['DBInstance']]
    print(items)
    # print(result)

    return result

params1 = {
    'DBInstanceId': 'rr-2zef3xsins46n6dlk'
}

query(params1)
