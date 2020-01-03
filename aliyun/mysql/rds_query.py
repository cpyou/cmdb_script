# 查询所有实例
import json
from conf import aliyun_conf


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_PageNumber(data.get('page', 1))
    request.set_PageSize(data.get('size', 10))
    if data.get('DBInstanceId', None) is not None:
        request.set_DBInstanceId(data['DBInstanceId'])

    # 发起API请求并显示返回值
    # response = client.do_action(request)
    # return response
    try:
        response = client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
    except ServerException as e:
        if e.http_status == 400 and e.error_code == 'InvalidDBInstanceId.NotFound':
            result = {'PageNumber': 1, 'TotalRecordCount': 0, 'PageSize': 50, 'RequestId': e.request_id, 'Items': {'DBInstance': []}}
        else:
            raise e

    print(result)

    return result


def main():
    params1 = {
        'DBInstanceId': 'rm-2ze2gz1hsx792391h'
    }

    result = query(params1)
    print(result['Items']['DBInstance'][0].keys())


if __name__ == '__main__':
    main()
