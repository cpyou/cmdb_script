#!/usr/bin/python
from conf import aliyun_conf
from aliyun.base.oss import *


def query(data):
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    cli = SDKOss(access_key_id, access_key_secret, region_id)
    result = cli.list_buckets()
    # result = cli.create_bucket('cpy-test111')
    # result = cli.delete_bucket('cpy-test111')

    print(result)


query({})
