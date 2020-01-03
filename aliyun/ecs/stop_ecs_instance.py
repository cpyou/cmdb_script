# 启动一台实例
import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient

    from aliyunsdkecs.request.v20140526 import StopInstanceRequest
    request = StopInstanceRequest.StopInstanceRequest()
    request.set_InstanceId(data.get('InstanceId'))

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
    'InstanceId': 'i-2zeh34kvwhgi0ikrryof'
}
query(data1)
