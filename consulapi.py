
import consulate
from consulate.models import agent

consul = consulate.Consul(host='')
consul.agent.checks()

services = consul.agent.services()

consul.agent.service.register(
    name='node_exporter11',
    service_id='node_bjc--base-cpytest-600',
    address='',
    port=9090,
    tags=["idc=bjc", "org=", "group=base", "app=cpytest", "server=bjc--base-cpytest-600"],
    meta=None,
    check=None,
    checks=[
        # {
        #     "tcp": "172.16.71.73:80",
        #     "interval": "60s"
        #  }
    ],
    enable_tag_override=None
)

consul.agent.service.register(
    name='node_exporter11',
    service_id='node_exporter-bjc--base-cpytest-601',
    address='',
    port=9090,
    tags=["idc=bje", "org=", "group=base", "app=cpytest", "server=bjc--base-cpytest-601"],
    meta=None,
    check=None,
    checks=[agent.Check(name='test1', tcp=":80", interval='60s')],
    enable_tag_override=None
)


consul.agent.service.deregister(service_id='node_exporter-bjc--base-cpytest-600')
