import sys, json, re, urllib.request

BASE = sys.argv[1].rstrip('/')

def req(method, path, obj=None, token=None):
    data = json.dumps(obj).encode() if obj is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        r.add_header('Content-Type', 'application/json')
    if token:
        r.add_header('token', token)
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.loads(f.read().decode())

cfg = json.load(open(r'D:\ctf-index\_z_496_remote.json'))
tok = cfg['tok']
preds = json.load(open(r'D:\ctf-index\_z_496_pred.json'))
pid = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'diag', 'body': 'b'}, tok)
em = req('GET', '/api/email/' + pid, None, tok)
got = int(re.search(r'boundary="=+(\d+)=+"', em['data']).group(1))
print('probe', got)
for i, p in enumerate(preds):
    if p == got:
        print('MATCHES preds[%d]  -> randrange offset %d' % (i, i))
        break
else:
    print('no match')
