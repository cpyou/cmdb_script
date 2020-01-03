# 查询所有实例
import json
import config


def query(data):
    from aliyunsdkcore.client import AcsClient
    # from aliyunsdkecs.request.v20140526 import AddTagsRequest
    from aliyunsdkecs.request.v20140526 import RemoveTagsRequest
    # 公司测试key
    access_key_id = config.AccessKeyID
    access_key_secret = config.AccessKeySecret
    region_id = config.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    # request = AddTagsRequest.AddTagsRequest()
    request = RemoveTagsRequest.RemoveTagsRequest()

    request.set_ResourceType(data.get('resource_type'))
    request.set_ResourceId(data.get('resource_id'))
    tags = data.get('tags', [])
    for i in range(len(tags)):
        request.add_query_param('Tag.{}.Key'.format(i + 1), tags[i]['key'])
        request.add_query_param('Tag.{}.Value'.format(i + 1), tags[i]['value'])
    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))

    print(result)

    return result


params1 = {
    'resource_type': 'instance',
    'resource_id': 'i-2ze4wr7ipjf33kfinljw',
    'tags': [{'key': "ops1", 'value': '运维平台1'}],
}
query(params1)
