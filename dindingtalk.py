"""
钉钉机器人消息接口
"""
import requests


class DingDingTalk:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "charset": "utf-8",
        }

    @staticmethod
    def generate_markdown_text(subject, content):
        markdown_text = "#### **【zabbix】" + subject + "**\n"
        for line in content.split("\n"):
            markdown_text += "> " + line + "\n\n"
        return markdown_text

    def send_data(self, subject, content):
        send_url = f'https://oapi.dingtalk.com/robot/send?access_token={self.token}'
        markdown_text = self.generate_markdown_text(subject, content)
        send_values = {
            "msgtype": "markdown",
            "markdown": {
                "title": subject,
                "text": markdown_text,
            },
            "at": {
                "atMobiles": [
                ],
                "isAtAll": False,
            }
        }

        r = requests.post(send_url, json=send_values, headers=self.headers)
        result = r.json()
        print(result)
        return result


def main():
    dingtalk_token = ""
    subject = "测试请忽略"
    content = """
告警项目：Free disk space is less than 10% on volume /mnt
告警机器：
当前状态：OK 值=14.18 %
----------分界线----------
故障共持续：8m
故障时间：2020.06.04 14:41:00
恢复时间：2020.06.04 14:49:01
事件ID：60538542
"""

    cli = DingDingTalk(dingtalk_token)
    cli.send_data(subject, content)


if __name__ == '__main__':
    main()
