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
        workflow_ids = list(set([item['properties']['workflow_instance_id']
                                 for item in assets if item['properties'].get('workflow_instance_id')]))
        wf_dict = self.get_wf(workflow_ids)
        project_ids = [v['properties']['project'] for k, v in wf_dict.items()]
        p_dict = self.get_projects(project_ids)
        group_ids = [v['group'] for k, v in p_dict.items()]
        g_dict = self.get_groups(group_ids)
        tag_ids = []
        [tag_ids.extend(item['asset_tags']) for item in assets]
        tag_dict = self.get_tags(tag_ids)
        asset_diffs = self.gen_asset_diffs(
            assets=assets, wf_dict=wf_dict, p_dict=p_dict, g_dict=g_dict, tag_dict=tag_dict)
        self.gen_excel(asset_diffs)

    def get_assets(self):
        params = {
            'asset_type': 'ALIYUN_ECS',
            'properties__instance_charge_type': 'PostPaid',
            'date_created__gte': '2019-06-22 00:00:00',
            'size': '500',
        }

        result = requests.get(f'{DOMAIN}/api/v1/cmdb/asset', params=params, headers=self.headers).json()

        assets = result['data']['items']
        return assets

    def get_wf(self, workflow_ids):
        wf_params = {
            'id__in': json.dumps(workflow_ids),
            'size': '500',
        }
        workflow_result = requests.get(f'{DOMAIN}/api/v1/workflow/?',
                                       params=wf_params, headers=self.headers).json()
        wf_dict = {}
        for wf in workflow_result['data']['items']:
            wf_dict[wf['id']] = wf
        return wf_dict

    def get_projects(self, project_ids):
        params = {
            'id__in': json.dumps(project_ids),
            'size': '500',
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
            'size': '500',
        }
        workflow_result = requests.get(f'{DOMAIN}/api/v2/group/?',
                                       params=params, headers=self.headers).json()
        data = {}
        for item in workflow_result['data']['items']:
            data[item['id']] = item
        return data

    def get_tags(self, tag_ids):
        params = {
            'id__in': json.dumps(tag_ids),
            'size': '500',
        }
        workflow_result = requests.get(f'{DOMAIN}/api/v2/tag/?',
                                       params=params, headers=self.headers).json()
        data = {}
        for item in workflow_result['data']['items']:
            data[item['id']] = item
        return data

    @staticmethod
    def gen_asset_diffs(assets, wf_dict, p_dict, g_dict, tag_dict):
        asset_data = []

        for asset in assets:
            asset_pay_type = asset['properties']['instance_charge_type']
            workflow_id = asset['properties'].get('workflow_instance_id')
            if not workflow_id:
                continue
            workflow_pay_type = wf_dict.get(workflow_id, {}).get('properties', {}).get('pay_type', '')
            project_id = wf_dict.get(workflow_id, {}).get('properties', {}).get('project', 0)
            project_key = p_dict.get(project_id, {}).get('key', '')
            group_id = p_dict.get(project_id, {}).get('group', 0)
            group_full_key = g_dict.get(group_id, {}).get('full_key')
            tag_id = asset['asset_tags'][0]
            tag_fullname = f'{tag_dict.get(tag_id)["key"]}:{tag_dict.get(tag_id)["value"]}'
            if asset_pay_type.upper() != workflow_pay_type.upper():
                asset_data.append({
                    'id': asset['id'],
                    'instance_id': asset['asset_id'],
                    'hostname': asset['name'],
                    'IP': asset['properties']['private_ip_address'][0],
                    'asset_pay_type': asset_pay_type,
                    'workflow_id': workflow_id,
                    'workflow_pay_type': workflow_pay_type,
                    'project_key': project_key,
                    'group_full_key': group_full_key,
                    'tag_fullname': tag_fullname,
                })
        return asset_data

    @staticmethod
    def gen_excel(asset_data):
        df = pd.DataFrame(asset_data)
        columns = ['id', 'instance_id', 'hostname', 'IP', 'asset_pay_type', 'workflow_id', 'workflow_pay_type',
                   'project_key', 'group_full_key', 'tag_fullname']
        df.to_excel('/Users/chenpuyu/Desktop/asset_diffs.xlsx', columns=columns)


if __name__ == '__main__':
    export_asset_diff_data = ExportAssetDiffData()
    export_asset_diff_data.run()
