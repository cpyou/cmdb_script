import json
import requests
import pandas as pd
from conf import tencent as tencent_conf
from tencent.base.cvm import TencentCvmSDKBase

TOKEN = ''
DOMAIN = ''


class AssetData(object):

    def __init__(self):
        token = TOKEN
        self.headers = {
            'AUTHORIZATION': 'Token {}'.format(token)
        }

    def run(self):
        assets = self.get_assets()
        asset_data = self.gen_asset_data(assets=assets)
        self.gen_excel(asset_data)
        print(assets)

    def get_assets(self):
        net_addrs = [
        ]
        result = []
        for net_addr in net_addrs:
            params = {
                'asset_type__in': json.dumps(['TENCENT_CVM']),
                'properties__status__in': json.dumps(['Running']),
                'properties__private_ip_address__0__startswith': net_addr,
                'size': 100000,
            }
            url = f'{DOMAIN}/api/v2/asset-openview/'
            r = requests.get(url, params=params, headers=self.headers)
            data = r.json()['data']['items']
            result.extend(data)
        return result

    @staticmethod
    def gen_asset_data(assets):
        asset_data = []

        for asset in assets:
            if asset['properties']['private_ip_address']:
                private_ip_address = asset['properties']['private_ip_address'][0]
            elif asset['properties']['innerip_address']['ip_address']:
                private_ip_address = asset['properties']['innerip_address']['ip_address'][0]
            else:
                print(asset)
                continue
            asset_data.append({
                'id': asset['id'],
                'asset_type': asset['asset_type'],
                'instance_id': asset['asset_id'],
                'hostname': asset['name'],
                'IP': private_ip_address,
                'env': asset['env'],
            })
        return asset_data

    @staticmethod
    def gen_excel(asset_diffs):
        # print(asset_diffs)
        df = pd.DataFrame(asset_diffs)
        columns = ['id', 'asset_type', 'instance_id', 'hostname', 'IP', 'env']
        df.to_excel('/Users/chenpuyu/Desktop/asset_data.xlsx', columns=columns)

    @staticmethod
    def stop_instances(instance_ids):
        cli = TencentCvmSDKBase(tencent_conf.secret_id, tencent_conf.secret_key, tencent_conf.region)
        result = cli.stop_instances({'InstanceIds': instance_ids})


if __name__ == '__main__':
    export_asset_data = AssetData()
    export_asset_data.run()
