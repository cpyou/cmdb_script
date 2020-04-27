# 查询lb
import json
from conf import aliyun_conf


def query(data):
    from aliyunsdkcore.client import AcsClient
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
    request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()

    # from aliyunsdkslb.request.v20140515 import DescribeVServerGroupsRequest
    # request = DescribeVServerGroupsRequest.DescribeVServerGroupsRequest()

    # from aliyunsdkslb.request.v20140515 import DescribeVServerGroupAttributeRequest
    # request = DescribeVServerGroupAttributeRequest.DescribeVServerGroupAttributeRequest()

    # from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRelatedEcsRequest
    # request = DescribeLoadBalancersRelatedEcsRequest.DescribeLoadBalancersRelatedEcsRequest()
    # from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest
    # request = DescribeHealthStatusRequest.DescribeHealthStatusRequest()
    if 'LoadBalancerId' in data:
        request.set_LoadBalancerId(data['LoadBalancerId'])

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)
    return result


def main():
    data = {
        'LoadBalancerId': ''
    }
    result = query(data)


if __name__ == '__main__':
    main()
