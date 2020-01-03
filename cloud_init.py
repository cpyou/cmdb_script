#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
1:挂载NAS
2:发送运维平台初始化

"""
import os
import logging
import logging.handlers
import sys
import traceback
import requests


# 参数定义
LOG_FILE = '/var/log/_cloud_int.log'
# LOG_FILE = '_cloud_int.log'
NAS_PATH = '6e6f04a9ac-mlh16.cn-qingdao.nas.aliyuncs.com:/'
MOUNT_CODE_PATH = '/data/web/'
CMDB_URL = ''
PROJECT_KEY = ''
CREDENTIAL_ID = 6
START_SERVICE_COMMAND = ''

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
fmt = '%(asctime)s: %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('_cloud_int')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info('开始初始化.....')


# 挂载NAS
def mount_nas():
    os.system('yum install nfs-utils -y')
    if not os.path.exists(MOUNT_CODE_PATH):
        os.system('mkdir {}'.format(MOUNT_CODE_PATH))
    return os.system('mount -t nfs4 {} {}'.format(NAS_PATH, MOUNT_CODE_PATH))


# 运维平台初始化
def send_cmdb_int():
    token = ''
    headers = {
        'AUTHORIZATION': token
    }
    url = '{}{}'.format(CMDB_URL, '/api/v2/service/ess_init/')
    instance_id = requests.get('http://100.100.100.200/latest/meta-data/instance-id').content
    payload = {
        "project_key": PROJECT_KEY,
        "instance_id": instance_id,
        "credential_id": CREDENTIAL_ID
    }
    return requests.post(url, json=payload, headers=headers)


if __name__ == '__main__':
    mount_status = mount_nas()
    if mount_status == 0:
        logger.info('挂载nas成功。')
    else:
        logger.error('挂载nas失败。')
    cmdb_res = send_cmdb_int()
    if cmdb_res.status_code == 200:
        logger.info('发送至运维平台执行成功。')
    else:
        logger.error('发送至运维平台执行失败。')
    logger.info('自定义任务完成。')
    logger.info('__main__完成。')
