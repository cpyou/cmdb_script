# 查询所有实例
import json
import config


def query(instance_id):
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
    from aliyunsdkdds.request.v20151201 import DescribeDBInstanceAttributeRequest
    request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
    request.set_DBInstanceId(instance_id)

    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result

query('dds-2ze538e0928ef794')

