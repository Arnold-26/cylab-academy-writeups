import sys, json, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = sys.argv[1].rstrip('/')
N = int(sys.argv[2]) if len(sys.argv) > 2 else 850
OUT = r'./_z_496_bounds.json'

def req(method, path, obj=None, token=None):
    data = json.dumps(obj).encode() if obj is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        r.add_header('Content-Type', 'application/json')
    if token:
        r.add_header('token', token)
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read().decode())

try:
    cfg = json.load(open(r'./_z_496_remote.json'))
except Exception:
    cfg = {}
if cfg.get('base') == BASE and cfg.get('tok'):
    pw, tok = cfg.get('pw'), cfg['tok']
    print('reuse token')
else:
    pw = req('GET', '/api/password')
    tok = req('POST', '/api/login', {'username': 'user@ses', 'password': pw})
    json.dump({'base': BASE, 'pw': pw, 'tok': tok}, open(r'./_z_496_remote.json', 'w'))
print('tok', tok[:12], 'pw', pw)

ids = []
lock = __import__('threading').Lock()
t0 = time.time()

def one(i):
    try:
        r = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'q%d' % i, 'body': 'b'}, tok)
        with lock:
            ids.append(r)
    except Exception as e:
        print('err', i, e)

with ThreadPoolExecutor(max_workers=12) as ex:
    list(ex.map(one, range(N)))
print('sent', len(ids), '%.1fs' % (time.time() - t0), flush=True)

emails = req('GET', '/api/emails', None, tok)
rows = []
for eid in ids:
    e = emails.get(eid)
    if not e:
        continue
    m = re.search(r'boundary="=+(\d+)=+"', e['data'])
    if not m:
        continue
    rows.append((e['time'], int(m.group(1))))
rows.sort()
times = [t for t, _ in rows]
print('rows', len(rows), 'dup times', len(times) - len(set(times)))
bounds = [b for _, b in rows]
json.dump(bounds, open(OUT, 'w'))
print('sample', bounds[:3], bounds[-2:])
