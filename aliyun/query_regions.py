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

    from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
    request = DescribeRegionsRequest.DescribeRegionsRequest()

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)
    return result


def main():
    result = query()
    print(result['Regions']['Region'][0].keys())
    print(result['Regions']['Region'][0])


if __name__ == '__main__':
    main()
