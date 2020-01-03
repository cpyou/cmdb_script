import json

from aliyunsdkcore.client import AcsClient
from aliyun.base import AliyunSDKBase


class KubernetesSDK(AliyunSDKBase):

    def __init__(self, region_id, access_key_id, access_key_secret):
        super(KubernetesSDK, self).__init__(region_id, access_key_id, access_key_secret)

    def describe_clusters(self, data=None):
        from aliyunsdkcs.request.v20151215 import DescribeClustersRequest
        request = DescribeClustersRequest.DescribeClustersRequest()

        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def describe_cluster_detail(self, cluster_id):
        from aliyunsdkcs.request.v20151215 import DescribeClusterDetailRequest
        request = DescribeClusterDetailRequest.DescribeClusterDetailRequest()
        request.set_ClusterId(cluster_id)

        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def create_cluster(self, data=None):
        from aliyunsdkcs.request.v20151215 import CreateClusterRequest
        request = CreateClusterRequest.CreateClusterRequest()
        request.add_header('Content-Type', 'application/json')
        # request.set_accept_format('json')
        request.set_content(json.dumps(data).encode('UTF-8'))
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def delete_cluster(self, cluster_id):
        from aliyunsdkcs.request.v20151215 import DeleteClusterRequest
        request = DeleteClusterRequest.DeleteClusterRequest()
        request.set_ClusterId(cluster_id)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result

    def describe_cluster_nodes(self, cluster_id, page=1, size=100):
        from aliyunsdkcs.request.v20151215 import DescribeClusterNodesRequest
        request = DescribeClusterNodesRequest.DescribeClusterNodesRequest()
        request.set_ClusterId(cluster_id)
        request.set_pageNumber(pageNumber=page)
        request.set_pageSize(pageSize=size)
        response = self.client.do_action_with_exception(request)
        result = json.loads(str(response, encoding="UTF-8"))
        return result
