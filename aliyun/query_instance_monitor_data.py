# 查询所有实例
import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    from aliyunsdkecs.request.v20140526 import DescribeInstanceMonitorDataRequest

    request = DescribeInstanceMonitorDataRequest.DescribeInstanceMonitorDataRequest()
    request.set_InstanceId(data.get('instance_id'))
    request.set_StartTime(data.get('StartTime'))
    request.set_EndTime(data.get('EndTime'))
    if data.get('instance_id'):
        pass

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result

params1 = {
    'instance_id': 'i-2ze1bnek6gl43jarwrj3',
    'StartTime': '2018-07-17T08:00:00Z',
    'EndTime': '2018-07-17T08:01:00Z',
}
query(params1)
