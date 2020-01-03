# 查询所有实例
import json
from conf import aliyun_conf


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkr_kvstore.request.v20150101 import DescribeInstanceAttributeRequest
    request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    # request.set_InstanceId(data.get('instance_id'))

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result


params1 = {
    # 'instance_id': 'r-bp115n76mm23ny57u2'
}
query(params1)
