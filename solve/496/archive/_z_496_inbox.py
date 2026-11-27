import sys, json, re, time, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')

BASE = sys.argv[1].rstrip('/')
u = urlparse(BASE)
conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)


def req(method, path, obj=None, token=None):
    body = json.dumps(obj) if obj is not None else None
    hdrs = {}
    if body is not None:
        hdrs['Content-Type'] = 'application/json'
    if token:
        hdrs['token'] = token
    conn.request(method, path, body=body, headers=hdrs)
    r = conn.getresponse()
    d = r.read().decode()
    if r.status >= 400:
        raise RuntimeError('%s %s %s' % (r.status, path, d[:200]))
    return json.loads(d)

cfg = json.load(open(r'./_z_496_remote.json'))
tok = cfg['tok']
emails = req('GET', '/api/emails', None, tok)
print('n emails', len(emails))
rows = []
for k, e in emails.items():
    d = e['data']
    subj = re.search(r'(?m)^Subject: (.*)$', d)
    frm = re.search(r'(?m)^From: (.*)$', d)
    rows.append((e['time'], k, frm.group(1).strip() if frm else None,
                 (subj.group(1).strip()[:60] if subj else None), len(d)))
rows.sort()
for t, k, f, s, n in rows:
    print('%.3f %s from=%-12s subj=%-60s %d' % (t, k[:8], f, s, n))
print('--- newest full ---')
t, k, f, s, n = rows[-1]
print(emails[k]['data'][:1500])
