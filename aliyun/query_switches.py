# 启动一台实例
import json

import config


def query():
    from aliyunsdkcore.client import AcsClient
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest
    request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
    request.set_PageNumber(2)
    request.set_PageSize(50)
    # VSwitchId = 'vsw-2zek4jt1uv0tc88oll7i6'
    # if VSwitchId:
    #     request.set_VSwitchId(VSwitchId)

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)
    return result


def main():
    result = query()


if __name__ == '__main__':
    main()
