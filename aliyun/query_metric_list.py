# 查询所有实例
import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcms.request.v20170301 import QueryMetricListRequest
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_PageNumber(data.get('page', 1))
    request.set_PageSize(data.get('size', 100))
    if data.get('instance_ids'):
        request.set_InstanceIds(data.get('instance_ids'))

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result

params1 = {
    # 'instance_ids': ['i-m5ejd5j1npj2p5izppy6']
    # 'instance_ids': ['i-m5e7ww79qca8uwk7gb6u']
    # 'instance_ids': ['i-m5ejd5j1npj166izqe19']
    # 'instance_ids': ['i-2zed9e2m3m1yde9p9gpl']
    # 'instance_ids': ['i-2zejc0rsr11bi5gxspkl']
    'instance_ids': ['i-2zec4zwwa24sfe6u6j73']
}
query(params1)
