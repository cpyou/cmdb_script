import requests

from tencent.cvm import TencentCvmSDKBase
from conf import tencent as tencent_conf


class SaltApi(object):
    def __init__(self, server_url, token):
        self.headers = {
            'X-Auth-Token': token
        }
        self.server_url = server_url
        self.cvm_cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)

    def init_server(self, ips, templates, playbook, playbook_args, create_user_name, cloud_type='tencent'):
        params = {
            'ips': ips,
            'templates': templates,
            'playbook': playbook,
            'playbook_args': playbook_args,
            'create_user_name': create_user_name,
            'cloud_type': cloud_type,
        }
        url = f'{self.server_url}/bootstrap'
        r = requests.post(url, json=params, headers=self.headers)
        return r.json()

    def get_host_ips(self, instance_ids):
        items = []
        count = len(instance_ids)
        start = 0
        end = 0
        while count > end:
            start += end
            end += 20
            tmp = self.cvm_cli.describe_instances({'InstanceIds': instance_ids[start:end]})
            items.extend(tmp['InstanceSet'])
