# encoding: utf-8
import datetime
from aliyun.log import LogClient, GetProjectLogsRequest
from prometheus_client import CollectorRegistry, push_to_gateway, Gauge

# endpoint = 'retention.cn-beijing-intranet.log.aliyuncs.com'

gateway = 'IP:9091'
endpoint = 'cn-beijing.log.aliyuncs.com'

accessKeyId = ''
accessKey = ''
project = '-php'  # 上面步骤创建的项目名称
logstore = '-php'  # 上面步骤创建的日志库名称

prometheus_metric = '_php_mysql_endpoint_error_test'  # 前端必填
metric_doc = 'mysqlerr'  #
job_label = '-php_dbname_error'
default_labels = {'info': '-php.dbname.error'}
select_str = "split_part(split_part(msg,':',4),'][',1) as dbname"
where_str = "msg='DBError'"

labels = ['info', 'dbname']


Now = datetime.datetime.today()
Start = Now - datetime.timedelta(minutes=1)
End = Now

StartTime = datetime.datetime.strftime(Start, '%Y-%m-%d %H:%M:00')
EndTime = datetime.datetime.strftime(End, '%Y-%m-%d %H:%M:00')

default_where_str = "AND __date__ >= '%s' and __date__ < '%s'".format(StartTime, EndTime)
query_str = "SELECT %s FROM %s WHERE  %s %s".format(select_str, logstore, where_str, default_where_str)

client = LogClient(endpoint, accessKeyId, accessKey)


def get_project_log(client, project, query_str):
    # 查询语句拼接
    req = GetProjectLogsRequest(project, query_str)
    res = client.get_project_logs(req)
    logs = res.get_logs()
    return logs


def push_prom():
    registry = CollectorRegistry()
    # 输出到Prometheus的metrics
    logs = get_project_log(client, project, logstore)
    g = Gauge(prometheus_metric, metric_doc, labels, registry=registry)
    for log in logs:
        contents = log.get_contents()
        value = contents.pop('value')
        contents.update(default_labels)
        g.labels(**contents).set(value)
    push_to_gateway(gateway, job=job_label, registry=registry)


if __name__ == '__main__':
    push_prom()
