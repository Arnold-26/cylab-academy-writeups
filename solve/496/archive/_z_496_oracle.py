"""Self-send oracle: POST a subject exactly like the bot's reply subject ('Re: ' + D)
and read back the raw bytes the SERVER's Python produced. Also reveals the current
MT19937 alignment (the boundary of the message is one of the predicted values)."""
import sys, json, re, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')
from _z_496_spec import make_D

BASE = sys.argv[1].rstrip('/')
B1 = sys.argv[2] if len(sys.argv) > 2 else '=' * 15 + '0123456789012345678' + '=='
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
        raise RuntimeError('%s %s %s %s' % (method, path, r.status, d[:300]))
    return json.loads(d)

cfg = json.load(open(r'./_z_496_remote.json'))
tok = cfg['tok']
preds = json.load(open(r'./_z_496_pred.json'))

D = make_D(B1)
subj = 'Re: ' + D
eid = req('POST', '/api/send', {'to': 'user@ses', 'subject': subj, 'body': 'oracle'}, tok)
em = req('GET', '/api/email/' + eid, None, tok)
data = em['data']
b = int(re.search(r'boundary="=+(\d+)=+"', data).group(1))
print('oracle boundary =', b)
for i, p in enumerate(preds):
    if p == b:
        print('   -> that is preds[%d] (next boundary will be preds[%d])' % (i, i + 1))
        break
else:
    print('   -> NOT in preds; alignment lost')
print('==== raw message (first 1200 bytes) ====')
print(repr(data[:1200]))
print()
print('==== header/body split ====')
i = data.find('\n\n')
print('first blank line at', i)
print(repr(data[max(0, i - 200):i + 60]))
