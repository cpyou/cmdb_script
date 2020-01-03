#!/usr/bin/python
from pprint import pprint

from conf import aliyun_conf
from aliyun.base.ess import *


access_key_id = aliyun_conf.AccessKeyID
access_key_secret = aliyun_conf.AccessKeySecret
region_id = aliyun_conf.region_id
cli = AliyunESS(access_key_id, access_key_secret, region_id)

# result = cli.create_scaling_rule(data)
# result = cli.execute_scaling_rules(data)
# result = cli.modify_scaling_rule(data)


create_arams = {
    'scaling_group_id': 'asg-bp15oubotmrqk2l4365m',
    'scaling_rule_name': f"手动执行-增加{2}台",
    'cooldown': 300,
    'scaling_rule_type': 'SimpleScalingRule',
    'adjustment_type': 'QuantityChangeInCapacity',
    'adjustment_value': 2,
}
# result = cli.create_scaling_group(create_arams)

exec_params = {
    'scaling_rule_ari': 'ari:acs:ess:cn-hangzhou:1930736016462079:scalingrule/asr-bp15oubotmrqnazs586i'
}
# result = cli.execute_scaling_rules(exec_params)
modify_params = {
    'scaling_rule_id': 'asr-bp1ftxdrm9go8lxzvnlg',
    'adjustment_value': 6,
}
# result = cli.modify_scaling_rule(modify_params)
query_params = {
    'scaling_group_id': 'asg-bp1j9e6hp4ibmzo4j8sw',
    'scaling_rule_name1': 'cmdb_scaling_rule',
}
# result = cli.describe_scaling_rules(query_params)
# pprint(result)

remove_instance_params = {
    'instance_ids': ['i-bp13dduprcf6te71fx1x'],
    'scaling_group_id': 'asg-bp1j9e6hp4ibmzo4j8sw',
}
result = cli.remove_instance(remove_instance_params)
pprint(result)
