#!/usr/bin/python
from pprint import pprint

from conf import aliyun_conf
from aliyun.base.ess import *


def query(data):
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    cli = AliyunESS(access_key_id, access_key_secret, region_id)
    result = cli.describe_scaling_configurations(data)
    # result = cli.create_scaling_configuration(data)
    # result = cli.modify_scaling_configurations(data)
    pprint(result)


create_params = {
    'scaling_group_id': 'asg-bp15oubotmrqk2l4365m',
    'instance_types': ["ecs.c5.xlarge", "ecs.sn1ne.xlarge", "ecs.sn1.large", "ecs.n4.xlarge"],
    'security_group_id': 'sg-bp165jsm55fjn3plkoh3',
    'image_name': 'ESS_IMAGE-prod-order-2019_12_10-21:58',
    'system_disk_category': 'cloud_efficiency',
    'system_disk_size': 50,
}
modify_params = {
    'scaling_configuration_id': 'asc-bp1ftxdrm9gn5uz7ijqy',
    'instance_types': ["ecs.c5.xlarge", "ecs.sn1ne.xlarge", "ecs.sn1.large", "ecs.n4.xlarge"],
    'security_group_id': 'sg-bp165jsm55fjn3plkoh3',
    'image_name': 'ESS_IMAGE-prod-order-2019_12_10-21:58',
    'system_disk_category': 'cloud_efficiency',
    'system_disk_size': 50,
}
query_params = {
    'scaling_group_id': 'asg-bp1b9j1vgdmw2iu7v4ne',
}
query(query_params)
