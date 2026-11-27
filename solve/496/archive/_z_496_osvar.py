import re, subprocess, os
os.chdir('/tmp/ostest')
raw = open('signed.eml').read()
B1 = '===============0344718024407626035=='
inj = ('From :admin@ses\n'
       '--' + B1 + ' \n'
       'Content-Type : text/html\n'
       'Content-Transfer-Encoding : base64\n'
       '\n'
       'PGltZyBzcmM9eCBvbmVycm9yPSJhbGVydCgxKSI+\n'
       '--' + B1 + '-- \n')
head, rest = raw.split('\n\n', 1)
variant = head + '\n' + inj + '\n' + rest
open('variant.eml', 'w').write(variant)
print('---- variant head ----')
print(variant[:900])
r = subprocess.run(['openssl', 'cms', '-verify', '-in', 'variant.eml', '-CAfile', 'cert.pem', '-out', 'out2.txt'],
                   capture_output=True, text=True)
print('rc', r.returncode)
print('err:', r.stderr.strip()[:500])
if os.path.exists('out2.txt'):
    print('out:', open('out2.txt').read()[:300])
