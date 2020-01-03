from aliyun.base.kubernetes import KubernetesSDK
from conf import aliyun_conf

if __name__ == '__main__':
    k8s_cli = KubernetesSDK(access_key_id=aliyun_conf.AccessKeyID,
                            access_key_secret=aliyun_conf.AccessKeySecret,
                            region_id=aliyun_conf.region_id)
    result = k8s_cli.describe_clusters()
    print(result)
