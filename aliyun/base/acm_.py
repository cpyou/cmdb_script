import acm
from conf import aliyun_conf
import json

ENDPOINT = "acm.aliyun.com"
NAMESPACE = "fea287d3-2f10-4e34-9f95-9ff1fb6b5165"

# get config
client = acm.ACMClient(ENDPOINT, NAMESPACE, aliyun_conf.AccessKeyID, aliyun_conf.AccessKeySecret)
print(client.list_all())
data_id = "test."
group = "DEFAULT_GROUP"
print(client.get(data_id, group))

data_id = 'test'
group = 'DEFAULT_GROUP1'
content = json.dumps({"b": "b"})
client.publish(data_id, group, content)
