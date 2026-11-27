"""Does the encoded-word round trip preserve D byte-exactly, including the leading
space on the injected `Content-Type : text/html` line?"""
import sys, json, subprocess
sys.path.insert(0, r'.')
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email._policybase import Policy as _P
_P.verify_generated_headers = False
from _z_496_spec import make_D, ews

B1 = '=' * 15 + '0753636783919971796' + '=='
B2 = '=' * 15 + '2525253071461182453' + '=='
D = make_D(B1, B2)
msg = MIMEMultipart()
msg['From'] = 'user@ses'
msg['To'] = 'admin@ses'
msg['Subject'] = ews(D) + "\nFrom :admin@ses"
msg.attach(MIMEText('hello'))
raw = msg.as_string()
open(r'./_z_496_emls\rt.eml', 'w', newline='', encoding='utf-8').write(raw)
r = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'node', './_z_496_parse.js',
                    './_z_496_emls/rt.eml'], capture_output=True, text=True)
j = json.loads(r.stdout)
sub = j.get('subject')
print('from  =', j.get('from'))
print('subject == D :', sub == D)
if sub != D:
    for i, (a, b) in enumerate(zip(sub or '', D)):
        if a != b:
            print('first diff at', i, repr((sub[m:] if False else sub)[max(0, i - 30):i + 30]),
                  '||', repr(D[max(0, i - 30):i + 30]))
            break
    else:
        print('length differs', len(sub or ''), len(D))
    print('sub repr head:', repr((sub or '')[:160]))
    print('D   repr head:', repr(D[:160]))
