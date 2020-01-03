#!/usr/bin/python
import json
import config
from aliyunsdkcore.client import AcsClient
from aliyunsdkemr.request.v20160408 import ListClustersRequest


def query(data):
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    clt = AcsClient(access_key_id, access_key_secret, region_id)  # set acessId and accessKey
    request = ListClustersRequest.ListClustersRequest()
    request.set_accept_format('json')
    # 设置状态过滤，只查找RUNNING和IDLE的集群，注意该参数为选填参数，可以不设置
    # request.add_query_param('StatusList.1', 'RUNNING')
    # request.add_query_param('StatusList.2', 'IDLE')
    response = clt.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))
    print(result)


query({})
