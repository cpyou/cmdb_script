import requests


class ApolloSDK(object):

    def __init__(self, host, username, password):
        self.host = host
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.session.post(url, data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.session.put(url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)

    def get_apps(self):
        """
        获取应用列表
        :return:
        """
        url = f'{self.host}/apps?appIds='
        return self.get(url).json()

    def get_app_info(self, app):
        """
        获取应用信息
        :param app:
        :return:
        """
        url = f'{self.host}/apps/{app}'
        return self.get(url).json()

    def get_app_navtree(self, app):
        """
        获取环境列表菜单
        :param app:
        :return:
        """
        url = f'{self.host}/apps/{app}/navtree'
        return self.get(url).json()

    def get_namespaces(self, app, env, cluster):
        """
        获取集群命名空间列表
        :param app:
        :param env:
        :param cluster:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces'
        return self.get(url).json()

    def get_namespace_info(self, app, env, cluster, namespace):
        """
        获取集群命名空间信息，及配置item信息
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}'
        return self.get(url).json()

    def get_namespace_item(self, app, env, cluster, namespace):
        """
        获取集群命名空间配置item信息
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/items'
        params = {
            'orderBy': 'lastModifiedTime',
        }
        return self.get(url, params=params).json()

    def get_namespace_active_release(self, app, env, cluster, namespace, page=0, size=1):
        """
        获取集群命名空间有效的配置, 默认取当前有效的配置
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :param page:
        :param size:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/releases/active'
        params = {
            'page': page,
            'size': size,
        }
        return self.get(url, params=params).json()

    def get_release_instance(self, env, release_id, page=0, size=20):
        """
        获取环境release实例列表
        :param env:
        :param release_id:
        :param page:
        :param size:
        :return:
        """
        url = f'{self.host}/envs/{env}/instances/by-release'
        params = {
            'page': page,
            'size': size,
            'releaseId': release_id,
        }
        return self.get(url, params=params).json()

    def get_release_histories(self, app, env, cluster, namespace, page=0, size=10):
        """
        获取发布历史
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :param page:
        :param size:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/releases/histories'
        params = {
            'page': page,
            'size': size,
        }
        return self.get(url, params=params).json()

    def publish(self, app, env, cluster, namespace, title, comment=''):
        """
        发布集群命名空间配置
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :param title: "20200212202220-release"
        :param comment:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/releases'
        payload = {
            'releaseTitle': title,
            'releaseComment': comment,
            'isEmergencyPublish': False,
        }
        return self.post(url, json=payload)

    def create_cluster(self, app, env, cluster_name):
        """
        创建集群
        :param app:
        :param env:
        :param cluster_name:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters'
        payload = {
            'name': cluster_name,
            'appId': app,
        }

        return self.post(url, json=payload).json()

    def create_appnamespaces(self, app, name, comment=""):
        """
        创建应用命名空间
        :param app:
        :param name:
        :param comment:
        :return:
        """
        url = f'{self.host}/apps/{app}/appnamespaces?appendNamespacePrefix=true'
        payload = {
            "appId": app,
            "name": name,
            "comment": comment,
            "isPublic": False,
            "format": "json"
        }
        return self.post(url, json=payload).json()

    def delete_appnamespace(self, app, namespace):
        """
        删除应用命名空间
        :param app:
        :param namespace:
        :return:
        """
        url = f'{self.host}/apps/{app}/appnamespaces/{namespace}'
        return self.delete(url)

    def delete_cluster_namespace(self, app, env, cluster, namespace):
        """
        删除集群命名空间
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}'
        return self.delete(url)

    def create_item(self, app, env, cluster, namespace, key, value, comment=''):
        """
        创建item
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :param key:
        :param value:
        :param comment:
        :return:
        """
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/item'
        payload = {
            "tableViewOperType": "create",
            "key": key,
            "value": value,
            "comment": comment,
            "addItemBtnDisabled": True,
        }
        return self.post(url, json=payload).json()

    def update_item(self, app, env, cluster, namespace, payload):
        """
        修改item
        :param app:
        :param env:
        :param cluster:
        :param namespace:
        :param payload: {
            "id":4012,
            "namespaceId":624,
            "key":"test_item2",
            "value":"test_item2",
            "comment":"test_item2__2",
            "lineNum":3,
            "dataChangeCreatedBy":"chenpuyu",
            "dataChangeLastModifiedBy":"chenpuyu",
            "dataChangeCreatedTime":"2020-02-13T21:39:51.000+0800",
            "dataChangeLastModifiedTime":"2020-02-13T21:39:51.000+0800",
            "tableViewOperType":"update"
            }
        :return:
        """
        import json
        url = f'{self.host}/apps/{app}/envs/{env}/clusters/{cluster}/namespaces/{namespace}/item'
        return self.put(url, data=json.dumps(payload), headers=self.headers, allow_redirects=False)
