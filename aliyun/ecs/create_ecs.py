# 创建ecs 实例
import json
from conf import aliyun_conf


def create(data):
    """
    创建ECS实例
    Args:data: {
        image_id: 'alinux_17_01_64_20G_cloudinit_20171222.vhd'
        instance_type: 'ecs.t1.small'
        instance_name: 'MyInstance'
        group_id: '安全组代码'
        switch_id: '虚拟交换机 ID'
        system_disk: {'name': 系统盘名称, 'category': 系统盘类别, 'size': 系统盘大小G, 'description': 系统盘描述}
        data_disks: [{'DiskName': 数据盘名称, 'Description': 数据盘描述, 'Category': 磁盘种类, 'Size': 容量大小}]
        }
    Returns:

    """

    from aliyunsdkcore.client import AcsClient
    # from aliyunsdkcore.acs_exception.exceptions import ClientException
    # from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
    import hashlib
    import os
    token = hashlib.sha1(os.urandom(64)).hexdigest()

    AccessKeyID = aliyun_conf.AccessKeyID
    AccessKeySecret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(AccessKeyID, AccessKeySecret, region_id)
    # 创建 request，并设置参数
    request = CreateInstanceRequest.CreateInstanceRequest()
    request.set_ImageId(data.get('image_id'))
    request.set_InstanceName(data.get('instance_name'))
    request.set_SecurityGroupId(data.get('group_id'))
    request.set_InstanceType(data.get('instance_type'))
    request.set_InstanceChargeType('PrePaid')
    request.set_AutoRenew(True)
    request.set_ClientToken(token)
    request.set_VSwitchId(data.get('switch_id'))
    request.set_DataDisks(data.get('data_disks', []))
    if data.get('system_disk'):
        system_disk = data.get('system_disk')
        request.set_SystemDiskDiskName(system_disk['name'])
        request.set_SystemDiskCategory(system_disk['category'])
        request.set_SystemDiskSize(system_disk['size'])
        request.set_SystemDiskDescription(system_disk['description'])
    # 发起 API 请求并打印返回
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))
    print(result)
    return result


# 测试环境参数
data1 = {
    'image_id': 'centos_7_04_64_20G_alibase_201701015.vhd',
    'instance_type': 'ecs.xn4.small',
    'instance_name': 'ecs.xn4.small',
    'group_id': 'sg-m5e2yrzkul8991wd95vo',
    'switch_id': 'vsw-m5e3i6j92ll29e5os3o51',
}

create(data1)
