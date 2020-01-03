from rundeck.client import Rundeck
server = ''
SECRET_API_TOKEN = ''

rd = Rundeck(server=server, api_token=SECRET_API_TOKEN)
rd.list_projects()

project = 'prom-test-cpy'
rd.list_jobs(project)

export_job = rd.export_job('9392e0f8-e579-4aa1-aed3-836da55f0573', fmt='yaml')

import hashlib
hashlib.pbkdf2_hmac()


import_temp = '''
- defaultTab: summary
  description: ''
  executionEnabled: true
  loglevel: INFO
  name: cpytest123
  nodeFilterEditable: false
  schedule:
    month: '*'
    time:
      hour: '*'
      minute: 0/1
      seconds: '0'
    weekday:
      day: '*'
    year: '*'
  scheduleEnabled: true
  sequence:
    commands:
    - exec: ls
    keepgoing: false
    strategy: node-first
  uuid: 107794c0-45f5-4a71-86b4-43a00ed1ba16
'''
import_job = rd.import_job(import_temp, project=project, fmt='yaml', dupeOption='update')


