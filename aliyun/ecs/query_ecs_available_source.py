import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient

    from aliyunsdkecs.request.v20140526 import DescribeAvailableResourceRequest
    request = DescribeAvailableResourceRequest.DescribeAvailableResourceRequest()
    request.set_DestinationResource(data.get('destination_resource', ''))
    request.set_IoOptimized(data.get('io_optimized', ''))
    request.set_SystemDiskCategory(data.get('SystemDiskCategory', ''))
    request.set_NetworkCategory('Vpc')
    if data.get('ZoneId', ''):
        request.set_ZoneId(data.get('ZoneId', ''))

    if data.get('cores'):
        request.add_query_param('Cores', data.get('cores', ''))
    if data.get('memory'):
        request.add_query_param('Memory', data.get('memory', ''))

    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)
    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    data = json.loads(str(response, encoding="UTF-8"))

    print(data)

    return data

data1 = {
    # 'destination_resource': 'SystemDisk',
    'destination_resource': 'InstanceType',
    'io_optimized': 'optimized',
    'SystemDiskCategory': 'cloud_efficiency',
    'ZoneId': 'cn-beijing-f',
    'cores': 2,
    'memory': 4,
}
query(data1)
