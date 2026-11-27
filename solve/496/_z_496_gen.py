"""Reproduce exactly how the reply's header block is serialized by the server's
Python email generator, for the new payload D (leading blank line)."""
import sys
sys.path.insert(0, r'.')
import email, email.generator as G
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email._policybase import Policy as _P
_P.verify_generated_headers = False
from _z_496_spec import make_D, make_subj, PWN, BODY

B1 = '=' * 15 + '2152839415017920306' + '=='
D = make_D(B1)
print('python', sys.version)
print('compat32._fold present:', hasattr(email.policy.compat32, '_fold'))

# the bot's reply: MIMEMultipart() + attach(MIMEText(content)) + attach(MIMEText(content,'html'))
msg = MIMEMultipart()
msg['From'] = 'admin@ses'
msg['To'] = 'admin@ses'
msg['Subject'] = 'Re: ' + D
msg.attach(MIMEText('BODYPLAIN'))
msg.attach(MIMEText('BODYHTML', 'html'))
try:
    raw = msg.as_string()
    print('as_string OK, len', len(raw))
    i = raw.index('Subject:')
    print('---- header block repr ----')
    print(repr(raw[:i + 400]))
except Exception as e:
    print('as_string RAISED:', type(e).__name__, e)

print()
print('==== emulate smail.sign_message outer wrapper ====')
try:
    from email.mime.base import MIMEBase
    inner = msg
    headers = {}
    copied = email.message_from_string(inner.as_string())
    for h in ['From', 'To', 'Subject']:
        headers[h] = copied.get_all(h)
        del copied[h]
    new_msg = MIMEMultipart('signed', protocol='application/pkcs7-signature', micalg='sha-256')
    for hdr, vals in headers.items():
        for v in vals:
            new_msg.add_header(hdr, str(v))
    new_msg.preamble = 'This is an S/MIME signed message'
    new_msg.attach(copied)
    sig = MIMEBase('application', 'pkcs7-signature', name='smime.p7s')
    sig.add_header('Content-Transfer-Encoding', 'base64')
    sig.add_header('Content-Disposition', 'attachment', filename='smime.p7s')
    sig.__delitem__('MIME-Version')
    sig.set_payload('QUJD')
    new_msg.attach(sig)
    try:
        out = new_msg.as_string()
        print('outer as_string OK, len', len(out))
        j = out.index('Subject:')
        print(repr(out[:j + 300]))
    except Exception as e:
        print('outer RAISED:', type(e).__name__, e)
except Exception as e:
    print('emulation failed:', type(e).__name__, e)
