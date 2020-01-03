#!/usr/bin/python
from pprint import pprint

from conf import aliyun_conf
from aliyun.base.ess import *


def query(data):
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    cli = AliyunESS(access_key_id, access_key_secret, region_id)
    result = cli.describe_scaling_groups(data)
    # result = cli.describe_scaling_configurations(data)
    # result = cli.describe_scaling_rules(data)
    # pprint(result)

    pprint(result['ScalingGroups']['ScalingGroup'][0])
    # pprint(result['ScalingGroups']['ScalingGroup'][1])


params = {
    # 'scaling_group_id1': 'asg-bp17nzuqngtsyg2ay0yn',
    # 'page': 2,
}
query(params)
