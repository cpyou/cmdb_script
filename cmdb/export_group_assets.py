"""
导出分组资产数据
"""

import json
import requests
import pandas as pd

TOKEN = ''
DOMAIN = ''


class ExportAssetData(object):

    def __init__(self):
        token = TOKEN
        self.headers = {
            'AUTHORIZATION': 'Token {}'.format(token)
        }

    def run(self):
        group_id = 1286
        assets = self.get_group_assets(group_id=group_id)
        asset_data = self.gen_asset_data(assets=assets)
        self.gen_excel(asset_data)

    def get_group_assets(self, group_id):
        params = {
            'asset_type__in': json.dumps(['ALIYUN_ECS']),
            'properties__status__in': json.dumps(['Running']),
            'size': 100000,
        }
        url = f'{DOMAIN}/api/v2/group/{group_id}/asset?'
        r = requests.get(url, params=params, headers=self.headers)
        result = r.json()
        data = result['data']['items']
        return data

    @staticmethod
    def gen_asset_data(assets):
        asset_data = []

        for asset in assets:
            print(asset['id'])
            private_ip_address = asset['properties']['private_ip_address'][0] if asset['properties'][
                'private_ip_address'] else asset['properties']['innerip_address']['ip_address'][0]
            asset_data.append({
                'id': asset['id'],
                'instance_id': asset['properties']['instance_type'],
                'hostname': asset['name'],
                'IP': private_ip_address,
                'env': asset['env'],
            })
        return asset_data

    @staticmethod
    def gen_excel(asset_data):
        print(asset_data)
        df = pd.DataFrame(asset_data)
        columns = ['id', 'instance_id', 'hostname', 'IP', 'env']
        df.to_excel('/Users/chenpuyu/Desktop/asset_data.xlsx', columns=columns)


if __name__ == '__main__':
    export_asset_data = ExportAssetData()
    export_asset_data.run()
