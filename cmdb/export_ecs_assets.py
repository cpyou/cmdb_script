"""
查询工单 资产支付类型和工单支付类型不一致的数据
"""

import json
import requests
import pandas as pd

TOKEN = ''
DOMAIN = ''


class ExportAssetDiffData(object):

    def __init__(self):
        token = TOKEN
        self.headers = {
            'AUTHORIZATION': 'Token {}'.format(token)
        }

    def run(self):
        assets = self.get_assets()
        project_ids = []
        for item in assets:
            project_ids.extend(item['projects'])
        project_ids = list(set(project_ids))
        p_dict = self.get_projects(project_ids)
        group_ids = [v['group'] for v in p_dict.values()]
        g_dict = self.get_groups(group_ids)
        user_ids = [v['owner'] for v in p_dict.values()]
        u_dict = self.get_users(user_ids)

        asset_diffs = self.gen_asset_diffs(
            assets=assets, p_dict=p_dict, g_dict=g_dict, u_dict=u_dict)
        self.gen_excel(asset_diffs)

    def get_assets(self):
        params = {
            'asset_type': 'ALIYUN_ECS',
            'properties__status': 'Running',
            'properties__creation_time__lte': '2018-07-01T00:00Z',
            'size': '10000',
        }

        result = requests.get(f'{DOMAIN}/api/v2/asset-openview/', params=params, headers=self.headers).json()

        assets = result['data']['items']
        return assets

    def get_projects(self, project_ids):
        params = {
            'id__in': json.dumps(project_ids),
            'size': '10000',
        }
        workflow_result = requests.get(f'{DOMAIN}/api/v2/project/?',
                                       params=params, headers=self.headers).json()
        data = {}
        for wf in workflow_result['data']['items']:
            data[wf['id']] = wf
        return data

    def get_groups(self, group_ids):
        params = {
            'id__in': json.dumps(group_ids),
            'size': '10000',
        }
        workflow_result = requests.get(f'{DOMAIN}/api/v2/group/?',
                                       params=params, headers=self.headers).json()
        data = {}
        for item in workflow_result['data']['items']:
            data[item['id']] = item
        return data

    def get_users(self, user_ids):
        params = {
            'id__in': json.dumps(user_ids),
            'size': '10000',
        }
        workflow_result = requests.get(f'{DOMAIN}/api/v1/cmdb/user?',
                                       params=params, headers=self.headers).json()
        data = {}
        for item in workflow_result['data']['items']:
            data[item['id']] = item
        return data

    @staticmethod
    def gen_asset_diffs(assets, p_dict, g_dict, u_dict):
        asset_diffs = []

        for asset in assets:
            project_id = asset.get('projects')[0]
            project_key = p_dict.get(project_id, {}).get('key', '')
            group_id = p_dict.get(project_id, {}).get('group', 0)
            user_id = p_dict.get(project_id, {}).get('owner', 0)
            group_full_key = g_dict.get(group_id, {}).get('full_key')
            username = u_dict.get(user_id, {}).get('first_name')
            private_ip_address = asset['properties']['private_ip_address'][0] if asset['properties']['private_ip_address'] else asset['properties']['innerip_address']['ip_address'][0]
            asset_diffs.append({
                'id': asset['id'],
                'instance_id': asset['asset_id'],
                'hostname': asset['name'],
                'IP': private_ip_address,
                'project_key': project_key,
                'group_full_key': group_full_key,
                'username': username,
                'creation_time': asset['properties']['creation_time'],
            })

        return asset_diffs

    @staticmethod
    def gen_excel(asset_diffs):
        print(asset_diffs)
        df = pd.DataFrame(asset_diffs)
        columns = ['id', 'instance_id', 'hostname', 'IP',
                   'project_key', 'group_full_key', 'username', 'creation_time']
        df.to_excel('/Users/chenpuyu/Desktop/asset_diffs.xlsx', columns=columns)


if __name__ == '__main__':
    export_asset_diff_data = ExportAssetDiffData()
    export_asset_diff_data.run()
