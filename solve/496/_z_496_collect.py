import sys, json, re, time, urllib.request

BASE = sys.argv[1].rstrip('/')
N = int(sys.argv[2]) if len(sys.argv) > 2 else 850

def req(method, path, obj=None, token=None):
    data = json.dumps(obj).encode() if obj is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        r.add_header('Content-Type', 'application/json')
    if token:
        r.add_header('token', token)
    with urllib.request.urlopen(r, timeout=30) as f:
        return json.loads(f.read().decode())

pw = req('GET', '/api/password')
if pw == 'already seen':
    print('PASSWORD ALREADY SEEN'); sys.exit(1)
tok = req('POST', '/api/login', {'username': 'user@ses', 'password': pw})
print('pw', pw); print('tok', tok)
json.dump({'base': BASE, 'pw': pw, 'tok': tok}, open(r'./_z_496_remote.json', 'w'))

ids = []
t0 = time.time()
for i in range(N):
    try:
        ids.append(req('POST', '/api/send', {'to': 'user@ses', 'subject': 'p%d' % i, 'body': 'b'}, tok))
    except Exception as e:
        print('send err at', i, e); break
    if i % 100 == 99:
        print('sent', i + 1, '%.1fs' % (time.time() - t0), flush=True)
print('sent total', len(ids), '%.1fs' % (time.time() - t0))

emails = req('GET', '/api/emails', None, tok)
print('emails', len(emails))
bounds = []
for eid in ids:
    data = emails[eid]['data']
    m = re.search(r'boundary="=+(\d+)=+"', data)
    bounds.append(int(m.group(1)) if m else None)
print('parsed', sum(1 for b in bounds if b is not None), 'of', len(bounds))
json.dump(bounds, open(r'./_z_496_bounds.json', 'w'))
print('first3', bounds[:3])
print('last3', bounds[-3:])
