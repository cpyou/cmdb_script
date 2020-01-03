import pandas as pd
from pandas import ExcelWriter
import requests

token = ''
headers = {
    'AUTHORIZATION': 'Token {}'.format(token)
}
file = '~/Desktop/REDIS.xlsx'

df = pd.read_excel(file)

with ExcelWriter('REDIS-df.xlsx') as w:
    df.to_excel(w)

# for i, row in df.iterrows():
#     project_key = row['project_key']
#     instance_id = row['instance_id']
#     project_params = {
#         'key': project_key
#     }
#     asset_params = {
#         'asset_type': 'ALIYUN_KVSTORE',
#         'asset_id': instance_id
#     }
#     project_url = 'https:///api/v2/project/'
#     asset_url = 'https:///api/v2/asset/'
#     project_result = requests.get(project_url, params=project_params, headers=headers).json()
#     asset_result = requests.get(asset_url, params=asset_params, headers=headers).json()
#     project_id = project_result['data']['items'][0].get('id')
#     if not project_id:
#         print('无项目', project_key)
#         continue
#     asset_id = asset_result['data']['items'][0].get('id')
#     if not asset_id:
#         print('无资产', instance_id)
#         continue
#
#     patch_data = {
#         'projects': [project_id]
#     }
    # project_patch_result = requests.patch(f'{asset_url}{asset_id}/', data=patch_data, headers=headers).json()
    # print(project_patch_result['code'])
