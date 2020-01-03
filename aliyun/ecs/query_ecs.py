# 查询所有实例
import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

from conf import aliyun_conf
import pandas as pd


def query(data):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
    # 公司测试key
    access_key_id = aliyun_conf.AccessKeyID
    access_key_secret = aliyun_conf.AccessKeySecret
    region_id = aliyun_conf.region_id
    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeInstancesRequest.DescribeInstancesRequest()
    page = data.get('page', 1)
    size = data.get('size', 100)
    request.set_PageNumber(page)
    request.set_PageSize(size)
    if data.get('instance_ids'):
        request.set_InstanceIds(data.get('instance_ids'))
    if data.get('PrivateIpAddresses'):
        request.set_PrivateIpAddresses(data.get('PrivateIpAddresses'))

    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    result = json.loads(str(response, encoding="UTF-8"))
    instances = result['Instances']['Instance']
    page += 1
    while page * size < result['TotalCount']:
        print(page, size)
        response = client.do_action_with_exception(request)
        tmp = json.loads(str(response, encoding="UTF-8"))
        instances.extend(tmp['Instances']['Instance'])
        page += 1
    # print(result)

    return instances


def gen_excel(asset_diffs):
    print(asset_diffs)
    fp = BytesIO()
    df = pd.DataFrame(asset_diffs)
    columns = ['InstanceId']
    df.to_excel(fp, columns=columns)
    fp.seek(0)
    return fp.read()


class SmtpEmail(object):

    def __init__(self, host, from_addr, password):
        self.from_addr = from_addr
        self.server = smtplib.SMTP_SSL(host, 465)
        self.server.login(from_addr, password)

    def send_email(self, to_addrs, subject, content, atts=None):
        atts = atts or []
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = ','.join(to_addrs)
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        if atts:
            for att_name, att_content in atts:
                att_text = MIMEText(att_content, 'base64', 'utf-8')
                att_text["Content-Type"] = 'application/octet-stream'
                att_text.add_header('Content-Disposition',  'attachment', filename=('utf-8', '', att_name))
                msg.attach(att_text)
        self.server.sendmail(self.from_addr, to_addrs, msg.as_string())
        self.server.close()
        return True


def main():
    email_host = 'smtp.qq.com'
    from_addr = '***@qq.com'
    password = ''
    to_addrs = ['***@qq.com']
    subject = f'阿里云实例列表-{str(datetime.date.today())}'
    content = subject
    attch_name = f'{subject}.xlsx'
    params2 = {
        'instance_ids': ['i-bp13dduprcf6te71fx1x'],
        # 'PrivateIpAddresses': ['172.16.112.228'],
    }
    result = query(params2)
    instance_ids = [item['InstanceId'] for item in result]
    params3 = {
        'instance_ids': instance_ids[:10],
    }
    result = query(params3)
    print(result)
    # attch_content = gen_excel(result)
    # atts = [(attch_name, attch_content)]
    # smtp_email = SmtpEmail(email_host, from_addr, password)
    # smtp_email.send_email(to_addrs=to_addrs, subject=subject, content=content, atts=atts)


if __name__ == '__main__':
    main()
