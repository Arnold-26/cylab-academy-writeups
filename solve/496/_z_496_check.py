import sys, json, subprocess, os, re, http.client
from urllib.parse import urlparse
sys.path.insert(0, r'.')
from _z_496_spec import PWN

BASE = sys.argv[1].rstrip('/')
u = urlparse(BASE)
conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=60)
conn.request('GET', '/api/root_cert')
r = conn.getresponse()
ca = r.read().decode()
open(r'./_z_496_emls\ca.crt', 'w', newline='').write(ca)
print('[i] root cert saved,', len(ca), 'bytes')

EML = './_z_496_emls/real_reply.eml'

r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'node',
                    './_z_496_parse.js', EML], capture_output=True, text=True)
j = json.loads(r.stdout)
print('[i] TOP parse: from=%r subject=%r' % (j.get('from'), j.get('subject')))
print('    html truthy:', bool(j.get('html')), '| html head:', repr((j.get('html') or '')[:80]))

r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'node', './_z_496_osverify.js',
                    EML, './_z_496_emls/ca.crt'], capture_output=True, text=True)
print('[i] openssl.wasm verify:')
print(r.stderr.strip()[:600])
so = '/tmp/os_stdout.txt'
r2 = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'bash', '-lc',
                     'cp /tmp/os_stdout.txt ./_z_496_emls/real_verified.eml; wc -c ./_z_496_emls/real_verified.eml'],
                    capture_output=True, text=True)
print('[i] verified content:', r2.stdout.strip())
r3 = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'node', './_z_496_parse.js',
                     './_z_496_emls/real_verified.eml'], capture_output=True, text=True)
try:
    j3 = json.loads(r3.stdout)
    print('[i] VERIFIED parse html == PWN:', j3.get('html') == PWN)
    print('    html head:', repr((j3.get('html') or '')[:120]))
    print('    text head:', repr((j3.get('text') or '')[:80]))
except Exception:
    print('[i] verified parse raw:', r3.stdout[:400], r3.stderr[:300])

print('[i] raw reply header block tail:')
data = open(r'./_z_496_emls\real_reply.eml', encoding='utf-8').read()
i = data.index('\n\n')
print(repr(data[max(0, i - 260):i + 40]))
