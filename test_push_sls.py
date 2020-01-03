#!/usr/bin/python
# encoding: utf-8
import datetime
from aliyun.log import *
from prometheus_client import CollectorRegistry, push_to_gateway, Gauge
from prpcrypt import encrypt, decrypt, get_default_salt, get_pass

salt = get_default_salt()

gateway = "IP:9091"
endpoint = "retention.cn-beijing-intranet.log.aliyuncs.com"

accessKeyId = ""
accessKey = get_pass(accessKeyId)
project = "-php"  # 上面步骤创建的项目名称
sls_logstore = "-php"  # 上面步骤创建的日志库名称

prometheus_metric = "_php_mysql_endpoint_error"
prometheus_metric_doc = "mysqlerr"
prometheus_job_label = "-php_dbname_error"
prometheus_default_labels = {'info': '-php.dbname.error', 'project_key': ''}
prometheus_labels = ['dbname']

sls_select_str = "split_part(split_part(msg,':',4),'][',1) AS dbname,COUNT(*) AS value"
sls_where_str = "msg='DBError'"
sls_group_by_str = "dbname"
sls_order_by_str = ""


Now = datetime.datetime.today()
Start = Now - datetime.timedelta(minutes=1)
End = Now

StartTime = datetime.datetime.strftime(Start, '%Y-%m-%d %H:%M:00')
EndTime = datetime.datetime.strftime(End, '%Y-%m-%d %H:%M:00')

sls_default_where_str = "AND __date__ >= '%s' and __date__ < '%s'" % (StartTime, EndTime)
sls_query_str = "SELECT %s FROM %s WHERE  %s %s " % (sls_select_str, sls_logstore, sls_where_str, sls_default_where_str)
if sls_group_by_str:
    sls_query_str += "group by %s " % sls_group_by_str
if sls_order_by_str:
    sls_query_str += "order by %s " % sls_order_by_str

client = LogClient(endpoint, accessKeyId, accessKey)


def get_project_log(client, project, sls_query_str):
    # 查询语句拼接
    req = GetProjectLogsRequest(project, sls_query_str)
    res = client.get_project_logs(req)
    logs = res.get_logs()
    return logs


def push_prom():
    registry = CollectorRegistry()
    # 输出到Prometheus的metrics
    logs = get_project_log(client, project, sls_query_str)
    g = Gauge(prometheus_metric, prometheus_metric_doc, prometheus_labels, registry=registry)
    for log in logs:
        contents = log.get_contents()
        value = contents.pop('value')
        contents.update(prometheus_default_labels)
        g.labels(**contents).set(value)
    push_to_gateway(gateway, job=prometheus_job_label, registry=registry)


if __name__ == '__main__':
    push_prom()
    