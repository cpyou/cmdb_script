import xlsxwriter

d = [
    ['ECS', ['ImageId', 'VlanId', 'EipAddress', 'ZoneId', 'IoOptimized', 'SerialNumber', 'Cpu', 'Memory', 'DeviceAvailable', 'SecurityGroupIds', 'SaleCycle', 'AutoReleaseTime', 'ResourceGroupId', 'OSType', 'OSName', 'InstanceNetworkType', 'HostName', 'CreationTime', 'EcsCapacityReservationAttr', 'RegionId', 'DeletionProtection', 'OperationLocks', 'ExpiredTime', 'InnerIpAddress', 'InstanceTypeFamily', 'InstanceId', 'NetworkInterfaces', 'InternetMaxBandwidthIn', 'CreditSpecification', 'InternetChargeType', 'SpotStrategy', 'StoppedMode', 'InternetMaxBandwidthOut', 'VpcAttributes', 'SpotPriceLimit', 'StartTime', 'KeyPairName', 'InstanceName', 'Description', 'OSNameEn', 'PublicIpAddress', 'InstanceType', 'Status', 'Recyclable', 'ClusterId', 'GPUSpec', 'InstanceChargeType', 'GPUAmount', 'DedicatedHostAttribute', 'DeploymentSetId']],
    ['RDS', ['LockMode', 'DBInstanceNetType', 'DBInstanceClass', 'ResourceGroupId', 'DBInstanceId', 'VpcCloudInstanceId', 'ZoneId', 'ReadOnlyDBInstanceIds', 'InstanceNetworkType', 'DBInstanceDescription', 'ConnectionMode', 'VSwitchId', 'VpcId', 'Engine', 'MutriORsignle', 'InsId', 'ExpireTime', 'CreateTime', 'DBInstanceType', 'RegionId', 'EngineVersion', 'LockReason', 'DBInstanceStatus', 'PayType']],
    ['Redis', ['Config', 'HasRenewChangeOrder', 'InstanceId', 'UserName', 'ZoneId', 'ArchitectureType', 'PrivateIp', 'VSwitchId', 'VpcId', 'NetworkType', 'PackageType', 'QPS', 'IsRds', 'EngineVersion', 'ConnectionDomain', 'InstanceName', 'Bandwidth', 'ChargeType', 'InstanceType', 'Tags', 'InstanceStatus', 'Port', 'InstanceClass', 'NodeType', 'RegionId', 'CreateTime', 'EndTime', 'Capacity', 'Connections']],
    ['Vpc', ['CreationTime', 'CidrBlock', 'VpcName', 'Status', 'Description', 'VSwitchIds', 'IsDefault', 'UserCidrs', 'RegionId', 'VRouterId', 'VpcId']],
    ['VSwitch', ['CreationTime', 'CidrBlock', 'Status', 'Description', 'IsDefault', 'ResourceGroupId', 'AvailableIpAddressCount', 'VSwitchName', 'ZoneId', 'VSwitchId', 'VpcId']],
]


def main():
    filename = '/Users/chenpuyu/Desktop/阿里云资源字段.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('阿里云')
    row = 0
    for asset_type, keys in d:
        row += 1
        worksheet.write_row(row, 0, [asset_type])
        row += 1
        worksheet.write_row(row, 0, keys)
        row += 1
    workbook.close()


def camel2underscore(jsondata):
    import re
    result = {}
    for (k, v) in jsondata.items():
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', k)
        k = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        result[k] = camel2underscore(v) if isinstance(v, dict) else v
    return result


def json_2_django_model(json_data):
    field_map = {
        str: "CharField(max_length=128)",
        int: "IntegerField(default=0)",
        float: "FloatField(default=0.0)",
        bool: "BooleanField(default=False)",
    }
    for field, v in camel2underscore(json_data).items():
        filed_type = field_map.get(type(v))
        if not filed_type:
            print(f'{field} = JSONField(default={type(v).__name__})')
            continue
        print(f'{field} = models.{filed_type}')


if __name__ == '__main__':
    # main()
    data = {'CreationTime': '2019-04-19T04:13:17Z', 'Tags': {'Tag': []}, 'SecurityGroupId': 'sg-2zecl59e6vt4vjqlkf8b', 'SecurityGroupName': 'security-group-20190419-dba-linshi', 'Description': 'dba传数据', 'ResourceGroupId': '', 'VpcId': 'vpc-2zeh81ixmvuusbihybhsb'}

    json_2_django_model(data)
