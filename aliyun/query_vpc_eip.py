import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    from aliyunsdkvpc.request.v20160428 import DescribeEipAddressesRequest
    request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
    request.set_PageNumber(1)
    if 'AllocationId' in data:
        request.set_AllocationId(data['AllocationId'])

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)
    return result


def main():
    data = {
        # 'AllocationId': 'eip-2zeb9q1hef2b0gagenecx'
    }
    result = query(data)
    print('')
    print(result['EipAddresses']['EipAddress'][0])


if __name__ == '__main__':
    main()
