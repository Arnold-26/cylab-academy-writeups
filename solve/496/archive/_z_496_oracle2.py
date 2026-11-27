import sys, json, re, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')
from _z_496_spec import make_D

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
    return r.status, d


cfg = json.load(open(r'./_z_496_remote.json'))
tok = cfg['tok']
D = make_D('=' * 15 + '1111111111111111111' + '==', '=' * 15 + '2222222222222222222' + '==')
st, d = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'Re: ' + D, 'body': 'fold'}, tok)
print('[i] POST /api/send with the exact reply-side subject ->', st, d[:200])
if st == 200:
    eid = json.loads(d)
    st, d = req('GET', '/api/email/' + eid, None, tok)
    raw = json.loads(d)['data']
    hdr = raw.split('\n\n', 1)[0]
    print('--- header block lines ---')
    for l in hdr.split('\n'):
        print(repr(l[:150]))
