from conf import fast_thread_conf

import requests

upload_url = f'https://api.fastthread.io/fastthread-api?apiKey={fast_thread_conf.apiKey}'

file = '/Users/chenpuyu/Downloads/xxx.log'
with open(file) as f:
    r = requests.post(upload_url, data=f, headers={'Content-Type': 'text'})
    print(r.json())
