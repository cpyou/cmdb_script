import hashlib
import json
import logging
import math
import os

from aliyun.base import AliyunSDKBase
from lib.utils import Pagination

logger = logging.getLogger('django')


class AliyunECS(AliyunSDKBase):

    def query(self, data):
        """
        查询一台或多台实例的详细信息
        文档: https://help.aliyun.com/document_detail/25506.html?spm=a2c4g.11186623.6.910.cXa6XW
        Args:
            data: {
                'page': 页码 默认1,
                'size': 页数 默认100,
                'instance_ids': ['实例id']
            }

        Returns:

        """
        instance_ids = data.get('instance_ids', [])
        logger.info('查询一台或多台实例的详细信息, 请求参数::%s', data)
        # 创建request，并设置参数
        from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageNumber(data.get('page', 1))
        request.set_PageSize(data.get('size', 100))
        if instance_ids:
            request.set_InstanceIds(data.get('instance_ids'))
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        if instance_ids:
            logger.info('查询到数据, 返回参数:%s', result)
        # id,instance_id,业务id,类型,地区,可用区,内网ip,外网ip,端口,cpu,内存,硬盘,价格
        return Pagination(**{
            'page': data.get('page', 1),
            'total': result['TotalCount'],
            'size': result['PageSize'],
            'items': result['Instances']['Instance']
        })

    def run_instance(self, data):
        """
        创建一台或多台 ECS 实例
        文档: https://help.aliyun.com/document_detail/63440.html?spm=a2c4g.11186623.6.901.xEnBGO
        Args: data: {
                image_id: 'alinux_17_01_64_20G_cloudinit_20171222.vhd'
                instance_type: 'ecs.t1.small'
                instance_name: 'MyInstance'
                hostname: '主机名'
                group_id: '安全组代码'
                switch_id: '虚拟交换机 ID'
                system_disk: {'name': 系统盘名称, 'category': 系统盘类别, 'size': 系统盘大小G, 'description': 系统盘描述}
                data_disks: [{'DiskName': 数据盘名称, 'Description': 数据盘描述, 'Category': 磁盘种类, 'Size': 容量大小}]
                }

        Returns:

        """
        logger.info('创建ECS实例, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import RunInstancesRequest
        import hashlib
        import os
        token = hashlib.sha1(os.urandom(64)).hexdigest()
        # 创建 request，并设置参数
        request = RunInstancesRequest.RunInstancesRequest()
        request.set_ImageId(data.get('image_id'))
        request.set_InstanceName(data.get('instance_name'))
        if data.get('KeyPairName'):
            request.set_KeyPairName(data.get('KeyPairName'))
        request.set_SecurityGroupId(data.get('security_group_id'))
        request.set_InstanceType(data.get('instance_type'))
        if data.get('pay_type') == 'PrePaid':
            request.add_query_param('InstanceChargeType', 'PrePaid')  # 实例的付费方式指定预付费
            request.add_query_param('Period', 1)
            request.add_query_param('AutoRenew', True)
            request.add_query_param('AutoRenewPeriod', data.get('renew_period', 1))  # 默认按一个月续费
        elif data.get('pay_type') == 'PostPaid':
            request.add_query_param('InstanceChargeType', 'PostPaid')  # 实例的付费方式指定按量付费
        else:
            assert False, '付费类型不支持'
        request.set_SecurityEnhancementStrategy('Active')  # 开启安全加固
        request.set_ClientToken(token)
        request.set_VSwitchId(data.get('switch_id'))
        if data.get('hostname'):
            request.set_HostName(data.get('hostname'))

        if data.get('zone_id'):
            request.set_ZoneId(data.get('zone_id'))
        request.set_DataDisks(data.get('data_disks', []))
        if data.get('system_disk'):
            system_disk = data.get('system_disk')
            request.set_SystemDiskCategory(system_disk['category'])
            request.set_SystemDiskSize(system_disk['size'])
            if system_disk.get('name'):
                request.set_SystemDiskDiskName(system_disk['name'])
            if system_disk.get('description'):
                request.set_SystemDiskDescription(system_disk['description'])
        # 发起 API 请求并打印返回
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('创建ECS实例, 返回参数:%s', result)
        return result

    def create(self, data):
        """
        创建ECS实例
        文档: https://help.aliyun.com/document_detail/25499.html?spm=a2c4g.11186623.6.902.m2Thql
        Args: data: {
                image_id: 'alinux_17_01_64_20G_cloudinit_20171222.vhd'
                instance_type: 'ecs.t1.small'
                instance_name: 'MyInstance'
                hostname: '主机名'
                group_id: '安全组代码'
                switch_id: '虚拟交换机 ID'
                system_disk: {'name': 系统盘名称, 'category': 系统盘类别, 'size': 系统盘大小G, 'description': 系统盘描述}
                data_disks: [{'DiskName': 数据盘名称, 'Description': 数据盘描述, 'Category': 磁盘种类, 'Size': 容量大小}]
                }

        Returns:

        """
        logger.info('创建ECS实例, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
        token = hashlib.sha1(os.urandom(64)).hexdigest()
        # 创建 request，并设置参数
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_ImageId(data.get('image_id'))
        request.set_InstanceName(data.get('instance_name'))
        request.set_KeyPairName(data.get('KeyPairName'))
        request.set_SecurityGroupId(data.get('group_id'))
        request.set_InstanceType(data.get('instance_type'))
        request.set_InstanceChargeType('PrePaid')  # 实例的付费方式指定预付费
        request.set_Period(1)
        request.set_SecurityEnhancementStrategy('Active')  # 开启安全加固
        request.set_AutoRenew(True)
        request.set_AutoRenewPeriod(data.get('renew_period', 1))  # 默认按一个月续费
        request.set_ClientToken(token)
        request.set_VSwitchId(data.get('switch_id'))
        if data.get('hostname'):
            request.set_HostName(data.get('hostname'))

        if data.get('zone_id'):
            request.set_ZoneId(data.get('zone_id'))
        request.set_DataDisks(data.get('data_disks', []))
        if data.get('system_disk'):
            system_disk = data.get('system_disk')
            request.set_SystemDiskCategory(system_disk['category'])
            request.set_SystemDiskSize(system_disk['size'])
            if system_disk.get('name'):
                request.set_SystemDiskDiskName(system_disk['name'])
            if system_disk.get('description'):
                request.set_SystemDiskDescription(system_disk['description'])
        # 发起 API 请求并打印返回
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def start_instance(self, instance_id):
        """
        启动一个实例
        文档: https://help.aliyun.com/document_detail/25500.html?spm=a2c4g.11186623.6.903.D1B2g8
        Args:
            instance_id: '实例id'

        Returns:

        """
        logger.info('ECS启动一个实例, 请求参数:%s', instance_id)
        from aliyunsdkecs.request.v20140526 import StartInstanceRequest
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(instance_id)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS启动一个实例, 返回参数:%s', result)
        return result

    def stop_instance(self, instance_id):
        """
        停止一个实例
        文档: https://help.aliyun.com/document_detail/25501.html?spm=a2c4g.11186623.6.904.KwxQJ7
        Args:
            instance_id: '实例id'

        Returns:

        """
        logger.info('ECS 停止一个实例, 请求参数:%s', instance_id)
        from aliyunsdkecs.request.v20140526 import StopInstanceRequest
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_InstanceId(instance_id)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 停止一个实例, 返回参数:%s', result)

        return result

    def reboot_instance(self, instance_id):
        """
        重启一个实例
        文档: https://help.aliyun.com/document_detail/25502.html?spm=a2c4g.11186623.6.1152.415715941vfilZ
        Args:
            instance_id: '实例id'

        Returns:

        """
        logger.info('ECS 重启一个实例, 请求参数:%s', instance_id)
        from aliyunsdkecs.request.v20140526 import RebootInstanceRequest
        request = RebootInstanceRequest.RebootInstanceRequest()
        request.set_InstanceId(instance_id)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 重启一个实例, 返回参数:%s', result)

        return result

    def modify_instance_attribute(self, data):
        """
        调用ModifyInstanceAttribute修改一台ECS实例的部分信息，包括实例密码、名称、描述、主机名和自定义数据等。如果是突发性能实例，可以切换这台实例的性能突发模式
        文档: https://help.aliyun.com/document_detail/25503.html?spm=a2c4g.11186623.6.1197.78be2eafYZ8MYW
        Args:
            data: {
                "instance_id": "",
                "instance_name": "",
                "host_name": "",
            }

        Returns:

        """
        logger.info('ECS 修改一个实例, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import ModifyInstanceAttributeRequest
        request = ModifyInstanceAttributeRequest.ModifyInstanceAttributeRequest()
        request = self.handle_params(request, data)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 重启一个实例, 返回参数:%s', result)

        return result

    def describe_disks(self, instance_id):
        """
        调用DescribeDisks查询一块或多块您已经创建的云盘以及本地盘。
        文档: https://help.aliyun.com/document_detail/25514.html?spm=a2c4g.11186623.6.1228.c98d1af2hHhszi
        Args:
            instance_id: '实例id'

        Returns:

        """
        logger.info('查询磁盘, 请求参数:%s', instance_id)
        from aliyunsdkecs.request.v20140526 import DescribeDisksRequest
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_InstanceId(instance_id)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('查询磁盘, 返回参数:%s', result)

        return result

    def apply_auto_snapshot_policy(self, disk_ids, policy_id):
        """
        调用ApplyAutoSnapshotPolicy为一块或者多块云盘应用自动快照策略。目标云盘已经应用了自动快照策略时，调用ApplyAutoSnapshotPolicy可以更换云盘当前应用的自动快照策略。
        文档: https://help.aliyun.com/document_detail/25531.html?spm=a2c4g.11186623.6.1263.291749baDOjpHp
        Args:
            disk_ids: '磁盘ids'
            policy_id: '自动快照策略id'

        Returns:

        """
        logger.info('调用自动快照策略, 请求参数:%s', disk_ids)
        from aliyunsdkecs.request.v20140526 import ApplyAutoSnapshotPolicyRequest
        request = ApplyAutoSnapshotPolicyRequest.ApplyAutoSnapshotPolicyRequest()
        request.set_diskIds(disk_ids)
        request.set_autoSnapshotPolicyId(policy_id)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('调用自动快照策略, 返回参数:%s', result)

        return result

    def query_instance_types(self, data=None):
        """
        查询云服务器 ECS 提供的实例规格资源
        文档: https://help.aliyun.com/document_detail/25620.html?spm=a2c4g.11186623.6.917.IlRj7b
        Args:
            data: {}

        Returns:

        """
        logger.info('ECS 查询云服务器 ECS 提供的实例规格资源, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        # logger.info('ECS 查询云服务器 ECS 提供的实例规格资源, 返回参数:%s', result)
        return result

    def query_available_source(self, data):
        """
        查询某一可用区的资源列表
        文档: https://help.aliyun.com/document_detail/66186.html?spm=a2c4g.11186623.2.1.AboTZn
        Args:
            data: {
                'destination_resource': 'InstanceType',
                'io_optimized': 'optimized',
                'system_disk_category': '系统盘类型: cloud, cloud_efficiency, cloud_ssd, ephemeral_ssd',
                'cores': '核心数',
                'memory': '内存大小G',
                'zone_id': '可用区id',
            }

        Returns:

        """
        logger.info('ECS 查询某一可用区的资源列表, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeAvailableResourceRequest
        request = DescribeAvailableResourceRequest.DescribeAvailableResourceRequest()
        request.set_DestinationResource(data.get('destination_resource', ''))
        request.set_IoOptimized(data.get('io_optimized', ''))
        if data.get('system_disk_category', ''):
            request.set_SystemDiskCategory(data.get('system_disk_category', ''))
        request.set_NetworkCategory('Vpc')
        if data.get('zone_id', ''):
            request.set_ZoneId(data.get('zone_id', ''))
        if data.get('cores'):
            request.add_query_param('Cores', data.get('cores', ''))
        if data.get('memory'):
            request.add_query_param('Memory', data.get('memory', ''))

        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 查询某一可用区的资源列表, 返回参数:%s', result)

        return result

    def query_regions(self, data=None):
        """
        查询您可以使用的阿里云地域
        文档: https://help.aliyun.com/document_detail/25609.html?spm=a2c4g.11186623.6.1022.hIFRSb
        Args:
            data: {
            }

        Returns:

        """
        logger.info('ECS 查询您可以使用的阿里云地域, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 查询您可以使用的阿里云地域, 返回参数:%s', result)
        return result

    def query_zones(self, data=None, sort_by_name=True):
        """
        查询一个阿里云地域下的可用区
        文档: https://help.aliyun.com/document_detail/25610.html?spm=a2c4g.11186623.6.1023.isMFAZ
        Args:
            data: {}
            sort_by_name:排序开关 默认True

        Returns:

        """
        logger.info('ECS 查询一个阿里云地域下的可用区, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeZonesRequest
        request = DescribeZonesRequest.DescribeZonesRequest()
        if data.get('RegionId', ''):
            request.add_query_param('RegionId', data.get('RegionId', ''))
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        if sort_by_name:
            zone = result.get('Zones', {}).get('Zone', [])
            zone.sort(key=lambda x: x.get('LocalName', ''))
        logger.info('ECS 查询一个阿里云地域下的可用区, 返回参数:%s', result)

        return result

    def query_images(self, data=None, sort_by_name=True):
        """
        查询您可以使用的镜像资源。
        文档: https://help.aliyun.com/document_detail/25534.html?spm=a2c4g.11186623.6.953.FrSWt8
        Args:
            data: {
                'page': 页码 默认1,
                'size': 页数 最大值50,
            }
            sort_by_name:排序开关 默认True

        Returns:

        """
        logger.info('ECS 查询您可以使用的镜像资源, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
        request = DescribeImagesRequest.DescribeImagesRequest()
        page = data.get('page', 1)
        page_size = data.get('size', 100)
        request.set_PageNumber(page)
        request.set_PageSize(page_size)
        # request.set_ImageOwnerAlias('self')
        if data.get('os_type'):
            request.set_OSType(data['os_type'])
        # 目前仅支持查询单个实例
        if data.get('instance_ids'):
            request.set_ImageId(data['instance_ids'][0])
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 查询您可以使用的镜像资源, 返回参数请求id:%s', result['RequestId'])
        # logger.info('ECS 查询您可以使用的镜像资源, 返回参数:%s', result)
        return Pagination(**{
            'page': data.get('page', 1),
            'total': result['TotalCount'],
            'size': result['PageSize'],
            'items': result['Images']['Image']
        })

    def create_image(self, instance_id, image_name):
        from aliyunsdkecs.request.v20140526 import CreateImageRequest
        request = CreateImageRequest.CreateImageRequest()
        request.set_InstanceId(instance_id)  # 设置需要镜像的ECS实例ID
        request.set_ImageName(image_name)  # 设置镜像名称，需唯一
        return self.send_request(request)

    def query_key_pairs(self, data=None):
        """
        查询一个或多个密钥对
        文档: https://help.aliyun.com/document_detail/51773.html?spm=a2c4g.11186623.6.990.XvayDh
        Args:
            data: {
                'page': 页码 默认1,
                'size': 页数 最大值50,
            }

        Returns:

        """
        logger.info('ECS 查询一个或多个密钥对, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeKeyPairsRequest
        request = DescribeKeyPairsRequest.DescribeKeyPairsRequest()
        request.set_PageNumber(data.get('page', 1))
        request.set_PageSize(data.get('size', 50))
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        logger.info('ECS 查询一个或多个密钥对, 返回参数:%s', result)
        return result

    def query_security_groups(self, data=None, sort_by_name=True):
        """
        查询您创建的安全组的基本信息，例如安全组 ID 和安全组描述等
        文档: https://help.aliyun.com/document_detail/25556.html?spm=a2c4g.11186623.6.979.z56cNW
        Args:
            data: {
                'page': 页码 默认1,
                'size': 页数 最大值50,
            }
            sort_by_name:排序开关 默认True


        Returns:

        """
        logger.info('ECS 查询您创建的安全组的基本信息, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
        request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        page = 1
        size = 50
        request.set_PageNumber(page)
        request.set_PageSize(size)

        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        total = result['TotalCount']
        max_page = math.ceil(total / size)
        page += 1
        while page <= max_page:
            request.set_PageNumber(page)
            response = self.client.do_action_with_exception(request)
            tmp = json.loads(str(response, encoding="UTF-8"))
            result['SecurityGroups']['SecurityGroup'].extend(tmp['SecurityGroups']['SecurityGroup'])
            page += 1
        result['PageSize'] = result.get('TotalCount')

        if sort_by_name:
            security_group = result.get('SecurityGroups', {}).get('SecurityGroup', [])
            security_group.sort(key=lambda x: x.get('SecurityGroupName', ''))
        # logger.info('ECS 查询您创建的安全组的基本信息, 返回参数:%s', result)
        return result

    def query_vpcs(self, data=None, sort_by_name=True):
        """
        查询已创建的VPC
        文档: https://help.aliyun.com/document_detail/35739.html?spm=a2c4g.11186623.2.6.yxJphd
        Args:
            data: {
                'page': 页码 默认1,
                'size': 页数 最大值50,
            }
            sort_by_name:排序开关 默认True

        Returns:

        """
        logger.info('ECS 查询已创建的VPC, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        page = 1
        page_size = 50
        request.set_PageNumber(page)
        request.set_PageSize(page_size)
        # 发起API请求并显示返回值

        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))

        total = result['TotalCount']
        max_page = math.ceil(total / page_size)
        page += 1
        while page <= max_page:
            request.set_PageNumber(page)
            response = self.client.do_action_with_exception(request)
            tmp = json.loads(str(response, encoding="UTF-8"))['Vpcs']['Vpc']
            result['Vpcs']['Vpc'].extend(tmp)
            page += 1
        result['PageSize'] = result.get('TotalCount')

        if sort_by_name:
            vpc = result.get('Vpcs', {}).get('vpc', [])
            vpc.sort(key=lambda x: x.get('VpcName', ''))
        # logger.info('ECS 查询一个阿里云地域下的可用区, 返回参数:%s', result)

        return result

    def query_v_switches(self, data=None, sort_by_name=True, vpc_id=None):
        """
        查询已创建的交换机
        文档: https://help.aliyun.com/document_detail/35748.html?spm=a2c4g.11186623.6.606.4DLHso
        Args:
            data:{
                'page': 页码 默认1,
                'size': 页数 最大值50,
            }
            sort_by_name:排序开关 默认True

        Returns:

        """
        logger.info('ECS 查询已创建的交换机, 请求参数:%s', data)
        from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        page = 1
        page_size = 50
        request.set_PageNumber(page)
        request.set_PageSize(page_size)
        if vpc_id:
            request.add_query_param('VpcId', vpc_id)
        # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))

        total = result['TotalCount']
        max_page = math.ceil(total / page_size)
        page += 1
        while page <= max_page:
            request.set_PageNumber(page)
            response = self.client.do_action_with_exception(request)
            tmp = json.loads(str(response, encoding="UTF-8"))
            result['VSwitches']['VSwitch'].extend(tmp['VSwitches']['VSwitch'])
            page += 1
        result['PageSize'] = result.get('TotalCount')
        if sort_by_name:
            switch = result.get('VSwitches', {}).get('VSwitch', [])
            switch.sort(key=lambda x: x.get('VSwitchName', ''))
        return result

    def add_ecs_tags(self, data):
        """
        创建标签
        文档: https://help.aliyun.com/document_detail/25616.html?spm=a2c4g.11174283.6.1013.2f8f52feQn4wPi
        Args:
            data:{
                'resource_id': 'i-2ze4wr7ipjf33kfinljw',
                'tags': [{'key': "ops", 'value': '运维平台'}],
            }

        Returns:

        """
        from aliyunsdkecs.request.v20140526 import AddTagsRequest
        request = AddTagsRequest.AddTagsRequest()

        request.set_ResourceType('instance')
        request.set_ResourceId(data.get('resource_id'))
        tags = data.get('tags', [])
        for i in range(len(tags)):
            request.add_query_param('Tag.{}.Key'.format(i + 1), tags[i]['key'])
            request.add_query_param('Tag.{}.Value'.format(i + 1), tags[i]['value'])
            # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def remove_ecs_tags(self, data):
        """
        删除标签
        文档: https://help.aliyun.com/document_detail/25617.html?spm=a2c4g.11186623.6.1014.794f2dfcarUjfO
        Args:
            data:{
                'resource_id': 'i-2ze4wr7ipjf33kfinljw',
                'tags': [{'key': "ops", 'value': '运维平台'}],
            }

        Returns:

        """
        from aliyunsdkecs.request.v20140526 import RemoveTagsRequest
        request = RemoveTagsRequest.RemoveTagsRequest()

        request.set_ResourceType('instance')
        request.set_ResourceId(data.get('resource_id'))
        tags = data.get('tags', [])
        for i in range(len(tags)):
            request.add_query_param('Tag.{}.Key'.format(i + 1), tags[i]['key'])
            request.add_query_param('Tag.{}.Value'.format(i + 1), tags[i]['value'])
            # 发起API请求并显示返回值
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def describe_instance_auto_renewal_attribute(self, renewal_status: str):
        """
        查询一台或多台预付费实例自动续费状态。
        https://help.aliyun.com/document_detail/52844.html
        Args:
            renewal_status:

        Returns:

        """
        from aliyunsdkecs.request.v20140526 import DescribeInstanceAutoRenewAttributeRequest
        request = DescribeInstanceAutoRenewAttributeRequest.DescribeInstanceAutoRenewAttributeRequest()
        request.add_query_param('PageSize', 100)
        request.add_query_param('RenewalStatus', renewal_status)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

