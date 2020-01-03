import consulate

from consulate.models import agent as models

# consul = consulate.Consul('')
# 测试机：bje--op-manager-test 172.16.71.73
consul = consulate.Consul('')

members = consul.agent.members()
services = consul.agent.services()
checks = consul.agent.checks()
metrics = consul.agent.metrics()
maintenance = consul.agent.maintenance()

hostname = 'qdc--ops-cmdb-03'
consul.agent.services().get(hostname, {})
consul.agent.checks().get('service:{}'.format(hostname), {})


name = 'node_exporter-cpy-test'
service_id = hostname
ip = '10.0.101.41'
port = 9100
idc, org, group, app, number = hostname.split('-')

tags = [
    'idc={}'.format(idc),
    'org={}'.format(org),
    'group={}'.format(group),
    'app={}'.format(app),
    'server={}'.format(hostname),
]

service_checks = [models.Check(name='test {}'.format(hostname), tcp="{}:{}".format(ip, port), interval="60s")]

a = [
    {
        "tcp": "{}:{}".format(ip, port),
        "interval": "60s"
    }
]
consul.agent.service.register(name, service_id=service_id, address=ip, port=port, tags=tags, checks=service_checks)
host_services = [(k, v) for k, v in consul.agent.services().items() if 'server={}'.format(hostname) in v.get('Tags')]
host_checks = [(k, v) for k, v in consul.agent.checks().items() if 'server={}'.format(hostname) in v.get('ServiceTags')]

consul.health.service('bje--op-rdb-2')
consul.agent.service.deregister(hostname)

