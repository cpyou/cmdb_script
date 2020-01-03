import hashlib
import os
from aliyun.base import AliyunSDKBase
from lib.utils import Pagination


class AliyunESS(AliyunSDKBase):

    @staticmethod
    def handle_page(request, data: dict):
        request.set_PageNumber(data.get('page', 1))
        request.set_PageSize(data.get('size', 50))
        return request

    def create_scaling_group(self, data: dict):
        """
        调用CreateScalingGroup创建一个伸缩组。
        https://help.aliyun.com/document_detail/25936.html?spm=a2c4g.11186623.6.656.358263167JWNjv
        :param data: {
            'scaling_group_name': 'cpy-test',
            'v_switch_ids': ['vsw-bp1vox7lg0nfbwzqc1vdl', 'vsw-bp19wnqnkvh0n59mwgll4'],
            'max_size': 0,
            'min_size': 0,
            'load_balancer_ids': [],
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import CreateScalingGroupRequest
        request = CreateScalingGroupRequest.CreateScalingGroupRequest()
        token = hashlib.sha1(os.urandom(64)).hexdigest()
        request.set_ClientToken(token)
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def describe_scaling_groups(self, data: dict):
        """
        调用DescribeScalingGroups查询伸缩组
        https://help.aliyun.com/document_detail/25938.html?spm=a2c4g.11186623.6.661.5adede6bZEHqEO
        :param data:
        :return:
        """
        from aliyunsdkess.request.v20140828 import DescribeScalingGroupsRequest
        request = DescribeScalingGroupsRequest.DescribeScalingGroupsRequest()
        self.handle_page(request, data)
        instance_ids = data.get('instance_ids')
        if instance_ids:
            for i in range(len(instance_ids)):
                request.add_query_param(f'ScalingGroupId.{i + 1}', instance_ids[i])
            data.pop('instance_ids')
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return Pagination(**{
            'page': data.get('page', 1),
            'total': result['TotalCount'],
            'size': result['PageSize'],
            'items': result['ScalingGroups']['ScalingGroup']
        })

    def modify_scaling_group(self, data: dict):
        """
        调用ModifyScalingGroup修改一个伸缩组。
        https://help.aliyun.com/document_detail/25937.html?spm=a2c4g.11186623.6.657.48cd40e3E8CbzF
        :param data: {
            'scaling_group_id': 'asg-bp15oubotmrqk2l4365m',
            'max_size': 0,
            'min_size': 0,
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import ModifyScalingGroupRequest
        request = ModifyScalingGroupRequest.ModifyScalingGroupRequest()
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def enable_scaling_group(self, data: dict):
        """
        调用EnableScalingGroup启用一个伸缩组
        https://help.aliyun.com/document_detail/25939.html?spm=a2c4g.11186623.6.658.a8e365a0RUoojn
        :param data: {
            'scaling_group_id': 'asg-bp15oubotmrqk2l4365m',
            'active_scaling_configuration_id': 'asc-bp1ftxdrm9gn5uz7ijqy',
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import EnableScalingGroupRequest
        request = EnableScalingGroupRequest.EnableScalingGroupRequest()
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def disable_scaling_group(self, data: dict):
        """
        调用DisableScalingGroup停用一个伸缩组。
        https://help.aliyun.com/document_detail/25940.html?spm=a2c4g.11186623.6.659.10d65d1dqGdfl9
        :param data:
        :return:
        """
        from aliyunsdkess.request.v20140828 import DisableScalingGroupRequest
        request = DisableScalingGroupRequest.DisableScalingGroupRequest()
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def describe_scaling_instances(self, data: dict):
        """
        调用DescribeScalingInstances查询伸缩组内ECS实例的列表，并列出ECS实例的信息。
        https://help.aliyun.com/document_detail/25942.html?spm=a2c4g.11186623.6.663.7e6a2e3aSPhBxL
        :param data:
        :return:
        """
        from aliyunsdkess.request.v20140828 import DescribeScalingInstancesRequest
        request = DescribeScalingInstancesRequest.DescribeScalingInstancesRequest()
        self.handle_page(request, data)
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def create_scaling_configuration(self, data: dict):
        """
        调用CreateScalingConfiguration创建一个伸缩配置。
        https://help.aliyun.com/document_detail/25944.html?spm=a2c4g.11186623.6.671.1bf1322eXYVJCe
        :param data: {
            'scaling_group_id': 'asg-bp15oubotmrqk2l4365m',
            'instance_types': ["ecs.c5.xlarge", "ecs.sn1ne.xlarge", "ecs.sn1.large", "ecs.n4.xlarge"],
            'security_group_id': 'sg-bp165jsm55fjn3plkoh3',
            'image_name': 'ESS_IMAGE-prod-order-2019_12_10-21:58',
            'system_disk_category': 'cloud_efficiency',
            'system_disk_size': 50,
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import CreateScalingConfigurationRequest
        request = CreateScalingConfigurationRequest.CreateScalingConfigurationRequest()
        security_group_ids = data.get('security_group_ids', [])
        if security_group_ids:
            for i in range(len(security_group_ids)):
                request.add_query_param(f'SecurityGroupIds.{i + 1}', security_group_ids[i])
            data.pop('security_group_ids')

        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def modify_scaling_configurations(self, data: dict):
        """
        调用ModifyScalingConfiguration修改一个伸缩配置。
        https://help.aliyun.com/document_detail/84770.html?spm=a2c4g.11186623.6.674.1bf1322e0N7c42
        :param data: {
            'scaling_configuration_id': 'asc-bp1ftxdrm9gn5uz7ijqy',
            'instance_types': ["ecs.c5.xlarge", "ecs.sn1ne.xlarge", "ecs.sn1.large", "ecs.n4.xlarge"],
            'security_group_id': 'sg-bp165jsm55fjn3plkoh3',
            'image_name': 'ESS_IMAGE-prod-order-2019_12_10-21:58',
            'system_disk_category': 'cloud_efficiency',
            'system_disk_size': 50,
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import ModifyScalingConfigurationRequest
        request = ModifyScalingConfigurationRequest.ModifyScalingConfigurationRequest()
        security_group_ids = data.get('security_group_ids', [])
        if security_group_ids:
            for i in range(len(security_group_ids)):
                request.add_query_param(f'SecurityGroupIds.{i + 1}', security_group_ids[i])
            data.pop('security_group_ids')
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def describe_scaling_configurations(self, data: dict):
        """
        调用DescribeScalingConfigurations查询现有的伸缩配置。
        https://help.aliyun.com/document_detail/25945.html?spm=a2c4g.11186623.6.672.7e6a2e3aZo479r
        :param data:
        :return:
        """
        from aliyunsdkess.request.v20140828 import DescribeScalingConfigurationsRequest
        request = DescribeScalingConfigurationsRequest.DescribeScalingConfigurationsRequest()
        self.handle_page(request, data)
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def create_scaling_rule(self, data: dict):
        """
        调用CreateScalingRule创建一条伸缩规则。
        https://help.aliyun.com/document_detail/25948.html?spm=a2c4g.11186623.6.676.524f291fdDdohN
        :param data:
        :return:
        """
        from aliyunsdkess.request.v20140828 import CreateScalingRuleRequest
        request = CreateScalingRuleRequest.CreateScalingRuleRequest()
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def describe_scaling_rules(self, data: dict):
        """
        调用DescribeScalingRules查询伸缩组下的伸缩规则，并列出伸缩规则的信息。
        https://help.aliyun.com/document_detail/25950.html?spm=a2c4g.11186623.6.679.70034a93YxxxWn
        :param data:
        :return:
        """
        from aliyunsdkess.request.v20140828 import DescribeScalingRulesRequest
        request = DescribeScalingRulesRequest.DescribeScalingRulesRequest()
        self.handle_page(request, data)
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def modify_scaling_rule(self, data: dict):
        """
        调用ModifyScalingRule修改一条伸缩规则。
        https://help.aliyun.com/document_detail/25949.html?spm=a2c4g.11186623.6.677.14431546uJpwhk
        :param data: {
            'scaling_rule_id': 'asr-bp15oubotmrqnazs586i',
            'adjustment_value': 4,
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import ModifyScalingRuleRequest
        request = ModifyScalingRuleRequest.ModifyScalingRuleRequest()
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    # 触发任务
    def execute_scaling_rules(self, data: dict):
        """
        调用ExecuteScalingRule执行一条伸缩规则。
        https://help.aliyun.com/document_detail/25953.html?spm=a2c4g.11186623.6.681.782d322eNV0XPL
        :param data: {
            'scaling_rule_ari': 'ari:acs:ess:cn-hangzhou:1930736016462079:scalingrule/asr-bp15oubotmrqnazs586i'
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import ExecuteScalingRuleRequest
        request = ExecuteScalingRuleRequest.ExecuteScalingRuleRequest()
        token = hashlib.sha1(os.urandom(64)).hexdigest()
        request.set_ClientToken(token)
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result

    def remove_instance(self, data: dict):
        """
        调用RemoveInstances从一个伸缩组里移出ECS实例。
        https://help.aliyun.com/document_detail/25955.html?spm=a2c4g.11186623.6.686.5acf1546wgN4zR
        :param data: {
            'instance_ids': ['i-bp13dduprcf6te71fx1x'],
            'scaling_group_id': 'asg-bp1j9e6hp4ibmzo4j8sw',
        }
        :return:
        """
        from aliyunsdkess.request.v20140828 import RemoveInstancesRequest
        request = RemoveInstancesRequest.RemoveInstancesRequest()
        self.handle_params(request, data)
        # 发起API请求并显示返回值
        result = self.send_request(request)
        return result
