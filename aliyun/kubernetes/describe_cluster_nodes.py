from aliyun.base.kubernetes import KubernetesSDK
from conf import aliyun_conf

if __name__ == '__main__':
    k8s_cli = KubernetesSDK(access_key_id=aliyun_conf.AccessKeyID,
                            access_key_secret=aliyun_conf.AccessKeySecret,
                            region_id=aliyun_conf.region_id)
    # cluster_id = 'c048a6327c9d5432b95b0485e5995bb53'
    cluster_id = 'c8344fa916bac4f1c97eea14bbb40dc8c'
    result = k8s_cli.describe_cluster_nodes(cluster_id)
    print(result)
