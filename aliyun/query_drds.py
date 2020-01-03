# 查询所有实例
import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkdrds.request.v20171016 import DescribeDrdsInstancesRequest
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    # region_id = config.region_id
    region_id = 'cn-zhangjiakou'
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeDrdsInstancesRequest.DescribeDrdsInstancesRequest()
    # request.set_PageNumber(data.get('page', 1))
    # request.set_PageSize(data.get('size', 100))

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result


def main():
    result = query({})
    print(result['Data']['Instance'])
    print(len(result['Data']['Instance']))


if __name__ == '__main__':
    main()
