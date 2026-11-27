import sys, json, time, urllib.request

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

cfg = json.load(open(r'./_z_496_remote.json'))
tok = cfg['tok']
if cfg.get('base') != BASE:
    print('WARN base mismatch', cfg.get('base'))

t0 = time.time()
print('bot run 1 ->', req('POST', '/api/admin_bot', None, tok), '%.1fs' % (time.time() - t0), flush=True)
time.sleep(1)
t0 = time.time()
print('bot run 2 ->', req('POST', '/api/admin_bot', None, tok), '%.1fs' % (time.time() - t0), flush=True)

for attempt in range(5):
    emails = req('GET', '/api/emails', None, tok)
    print('inbox', len(emails))
    for k, e in emails.items():
        d = e['data']
        if 'academy{' in d or 'picoCTF{' in d or 'pwned' in d:
            print('=== HIT ===')
            print(d[:3000])
            sys.exit(0)
    time.sleep(4)
print('no flag yet')
