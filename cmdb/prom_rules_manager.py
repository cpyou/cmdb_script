import json

import requests


class PromRuleManager(object):

    def __init__(self, url, token=None):
        self.url = url
        self.headers = {
            'AUTHORIZATION': 'Token {}'.format(token)
        }

    def run(self, project_keys, add_rules):
        project_ids = self.get_project_ids_by_keys(project_keys)
        print('获取到项目ids', project_ids)
        for project_id in project_ids:
            self.update_project_rule(project_id, add_rules)
            self.enable_rule(project_id)

    def get_project_ids_by_keys(self, project_keys):
        params = {
            'key__in': json.dumps(project_keys),
            'size': '10000',
        }
        result = requests.get(f'{self.url}/api/v2/project/?', params=params, headers=self.headers).json()
        project_ids = [item['id'] for item in result['data']['items']]

        return project_ids

    def update_project_rule(self, project_id, add_rules):
        result = requests.get(f'{self.url}/api/v1/alert_manager/{project_id}', headers=self.headers).json()

        new_rules = result['data'].get('rules', [])
        new_rules.extend(add_rules)
        payload = {
            'rules': new_rules,
            'state': 'disabled',
        }
        update_result = requests.patch(f'{self.url}/api/v1/alert_manager/{project_id}',
                                       json=payload, headers=self.headers).json()
        if update_result['code'] == 0:
            print(f'更新项目{project_id}报警规则成功')
        else:
            print(f'更新项目{project_id}报警规则失败')
        return True

    def enable_rule(self, project_id):
        params = {
            'state': 'enabled'
        }
        result = requests.patch(f'{self.url}/api/v1/alert_manager/{project_id}',
                                json=params, headers=self.headers).json()
        if result['code'] == 0:
            print(f'启用项目{project_id}报警规则成功')
        else:
            print(f'启用项目{project_id}报警规则失败')
        return True

    def disabled_rule(self, project_id):
        params = {
            'state': 'disabled'
        }
        result = requests.patch(f'{self.url}/api/v1/alert_manager/{project_id}',
                                json=params, headers=self.headers).json()
        if result['code'] == 0:
            print(f'禁用项目{project_id}报警规则成功')
        else:
            print(f'禁用项目{project_id}报警规则失败')
        return True


if __name__ == '__main__':
    url = ''
    token = ''
    project_keys = ['']
    rules = [
        {
            "alert": "报警标题",
            "expr": "报警语句",
            "for": "3m",
            "labels": {
                "severity": "average"
            },
            "annotations": {
                "summary": "报警概要",
                "description": "报警描述"
            }
        },
    ]
    prom_rule_manager = PromRuleManager(url, token)
    prom_rule_manager.run(project_keys, rules)
