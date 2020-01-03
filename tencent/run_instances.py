from tencent.cvm import TencentCvmSDKBase
from conf import tencent as tencent_conf

if __name__ == '__main__':
    cvm_cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
    params = {
        'Placement': {'Zone': 'ap-beijing-5'},
        'ImageId': 'img-9qabwvbn',
        'InstanceChargeType': 'PREPAID',
        'InstanceChargePrepaid': {'Period': 1, 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW'},
        'InstanceType': 'S4.MEDIUM4',
        'SystemDisk': {
            'DiskType': 'CLOUD_PREMIUM',
            'DiskSize': 100,  # 系统盘默认100G
        },
        'LoginSettings': {'KeyIds': ["skey-ddaf1kah"]},
        'VirtualPrivateCloud': {
            'VpcId': 'vpc-9pelc1ty',
            'SubnetId': 'subnet-822bl58x',
        }
    }
    result = cvm_cli.run_instances(params)
    print(result)
