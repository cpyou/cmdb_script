# 查询所有实例
import json

from conf import aliyun_conf


def query(instance_id):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkecs.request.v20140526 import DescribeDisksRequest
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeDisksRequest.DescribeDisksRequest()
    request.set_InstanceId(instance_id)

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    return result


def main():
    result = query('i-bp18yy8egbks0n0896il')
    print(result)


if __name__ == '__main__':
    main()
