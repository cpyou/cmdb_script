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
        assets = self.get_assets()
        asset_data = self.gen_asset_data(assets=assets)
        self.gen_excel(asset_data)

    def get_assets(self):
        params = {
            'asset_type__in': json.dumps(['ALIYUN_ECS', 'TENCENT_CVM']),
            'properties__status__in': json.dumps(['Running']),
            'size': 100000,
        }
        url = f'{DOMAIN}/api/v2/asset-openview/'
        r = requests.get(url, params=params, headers=self.headers)
        result = r.json()
        data = result['data']['items']
        return data

    @staticmethod
    def gen_asset_data(assets):
        asset_diffs = []

        for asset in assets:
            if asset['properties']['private_ip_address']:
                private_ip_address = asset['properties']['private_ip_address'][0]
            elif asset['properties']['innerip_address']['ip_address']:
                private_ip_address = asset['properties']['innerip_address']['ip_address'][0]
            else:
                print(asset)
                continue
            asset_diffs.append({
                'id': asset['id'],
                'asset_type': asset['asset_type'],
                'instance_id': asset['asset_id'],
                'hostname': asset['name'],
                'IP': private_ip_address,
                'env': asset['env'],
            })
        return asset_diffs

    @staticmethod
    def gen_excel(asset_diffs):
        # print(asset_diffs)
        df = pd.DataFrame(asset_diffs)
        columns = ['id', 'asset_type', 'instance_id', 'hostname', 'IP', 'env']
        df.to_excel('/Users/chenpuyu/Desktop/asset_data.xlsx', columns=columns)


if __name__ == '__main__':
    export_asset_data = ExportAssetData()
    export_asset_data.run()
