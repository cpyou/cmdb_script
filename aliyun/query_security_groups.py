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

    from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
    request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
    page = 1
    size = 50
    request.set_PageNumber(page)
    request.set_PageSize(size)

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    # 发起API请求并显示返回值
    # response = client.do_action_with_exception(request)
    # result = json.loads(str(response, encoding="UTF-8"))
    return result


def main():
    result = query()
    # print(result)
    print(result['SecurityGroups']['SecurityGroup'][0])


if __name__ == '__main__':
    main()
