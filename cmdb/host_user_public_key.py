import requests
import logging
import logging.handlers
import sys
import time
import traceback
import xlsxwriter

from datetime import datetime


LOG_FILE = 'host_key.log'
SYS_USER = 'lcsuper'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
fmt = '%(asctime)s: %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('host_key')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

server_url = ''
headers = {
    'Authorization': 'Token '
}


def get_assets(page, size):
    asset_url = '{}/api/v1/cmdb/asset'.format(server_url)
    play_load = {
        'asset_type': 'ALIYUN_ECS',
        'page': page,
        'size': size,
    }
    return requests.get(asset_url, play_load, headers=headers).json()


def get_host_keys(asset_ids):
    shell_url = '{}/api/v1/cmdb/asset/assets_shell'.format(server_url)
    play_load = {
        "args": [],
        "kwargs": {
            "asset_ids": asset_ids,
            "cmd": "cat /home/{}/.ssh/authorized_keys".format(SYS_USER),
            "module": "command",
        }
    }
    return requests.post(shell_url, json=play_load, headers=headers)


def write_sxlx():
    page = 1
    size = 20
    line = 1
    worksheet = workbook = xlsxwriter.Workbook('主机{}用户key列表.xlsx'.format(SYS_USER))
    worksheet = workbook.add_worksheet()
    try:
        pagination = get_assets(page, size)
        while pagination:
            logger.info(page)
            # logger.info(pagination)
            asset_ids = [item['id'] for item in pagination['data']['items']]
            flag = True
            times = 0
            while flag:
                times += 1
                try:
                    host_keys = get_host_keys(asset_ids).json()['data']
                    # logger.info('host_keys: %s', host_keys)
                    flag = False
                except:
                    logger.info('ansible 异常')
                    pass
                if times > 5:
                    logger.info('ansible 异常资产', asset_ids)
                    flag = False
            for item in pagination['data']['items']:
                if item['properties']['private_ip_address']:
                    ip_address = item['properties']['private_ip_address'][0]
                elif item['properties']['innerip_address']['ip_address']:
                    ip_address = item['properties']['innerip_address']['ip_address'][0]
                    if not ip_address:
                        continue
                worksheet.write(line, 0, item['name'])
                worksheet.write(line, 1, item['asset_id'])
                worksheet.write(line, 2, ip_address)
                if host_keys and host_keys[1]['ok'].get(ip_address):
                    stdout_lines = host_keys[1]['ok'][ip_address]['command']['stdout_lines']
                    key_i = 3
                    for l in stdout_lines:
                        key_name = l.split(' ')[2] if len(l.split(' ')) == 3 else ''
                        logger.info(key_name)
                        worksheet.write(line, key_i, key_name)
                        key_i += 1
                line += 1
            if pagination['data']['total'] > page * size:
                page += 1
                time.sleep(5)
                pagination = get_assets(page, size)
            else:
                pagination = False
    except:
        workbook.close()
    workbook.close()
    return True


if __name__ == '__main__':
    write_sxlx()
