# 启动一台实例
import json
from conf import aliyun_conf
from pprint import pprint


def query(data: dict):
    from aliyunsdkcore.client import AcsClient
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
    request = DescribeImagesRequest.DescribeImagesRequest()
    if data.get('image_id'):
        request.set_ImageId(data['image_id'])
    request.set_OSType('linux')
    # request.set_ImageOwnerAlias('self')
    request.set_PageSize(100)
    request.set_PageNumber(2)

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    # print(result)
    return result


if __name__ == '__main__':
    params = {
        # 'image_id': 'm-bp135nlsftzn7ikblmdo',
        # 'image_id': 'm-bp1a1rcx3i639zdxnkrd',
    }
    result = query(params)
    print(len(result['Images']['Image']))
    for item in result['Images']['Image']:
        # print(item['ImageName'])
        if 'vhd' in item['ImageId']:
            pprint(item)
            print()
