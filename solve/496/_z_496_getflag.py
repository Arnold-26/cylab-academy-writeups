import sys, json, http.client
from urllib.parse import urlparse
BASE = sys.argv[1].rstrip('/')
u = urlparse(BASE)
conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)
conn.request('GET', '/api/emails', headers={'token': json.load(open(r'./_z_496_remote.json'))['tok']})
r = conn.getresponse()
emails = json.loads(r.read().decode())
for k, e in emails.items():
    d = e['data']
    if 'pwned' in d:
        print('=== EMAIL', k, '===')
        print(d[:1600])
        print('...')
        i = d.find('\n\n', d.find('pwned'))
        print('BODY:', repr(d[i:i + 300]))
        open(r'./_z_496_emls\flag_mail.eml', 'w', newline='', encoding='utf-8').write(d)
