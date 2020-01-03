#!/usr/bin/python
from pprint import pprint

from conf import aliyun_conf
from aliyun.base.ess import *


access_key_id = aliyun_conf.AccessKeyID
access_key_secret = aliyun_conf.AccessKeySecret
region_id = aliyun_conf.region_id
cli = AliyunESS(access_key_id, access_key_secret, region_id)
# result = cli.describe_scaling_groups(data)
# result = cli.create_scaling_group(data)
# result = cli.enable_scaling_group(data)
# result = cli.modify_scaling_group(data)


create_params = {
    'scaling_group_name': 'cpy-test',
    'v_switch_ids': ['vsw-bp1vox7lg0nfbwzqc1vdl', 'vsw-bp19wnqnkvh0n59mwgll4'],
    'max_size': 0,
    'min_size': 0,
}
enable_params = {
    'scaling_rule_id': 'asg-bp15oubotmrqk2l4365m',
    'active_scaling_configuration_id': 'asc-bp1ftxdrm9gn5uz7ijqy',
}
modify_params = {
    'scaling_group_id': 'asg-bp15oubotmrqk2l4365m',
    'max_size': 0,
    'min_size': 0,
}
query_params1 = {
    'scaling_group_id1': 'asg-bp1j9e6hp4ibmzo4j8sw',
}
result = cli.describe_scaling_groups(query_params1)
query_params = {
    'scaling_group_id': 'asg-bp1j9e6hp4ibmzo4j8sw',
}
# result = cli.describe_scaling_instances(query_params)
# query(params)
pprint(result)
