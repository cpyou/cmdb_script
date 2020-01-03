import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient

    from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest
    request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()

    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)
    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)
    for d in result['InstanceTypes']['InstanceType']:
        print('%s-cpuCore:%s-memory%s' % (d['InstanceTypeId'], d['CpuCoreCount'], d['MemorySize']))
    print(len(result['InstanceTypes']['InstanceType']))

    return result

data1 = {
    'instance_ids': ['i-m5ehlmim4k7p8a0mi6ze']
}
query(data1)
