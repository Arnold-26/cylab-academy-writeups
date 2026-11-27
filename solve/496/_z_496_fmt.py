import email.generator as G, inspect
src = inspect.getsource(G)
for i, l in enumerate(src.splitlines(), 1):
    if '_fmt' in l or '_FMT' in l:
        print(i, l)
print('---')
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
m = MIMEMultipart()
m['From'] = 'u'
m.attach(MIMEText('x'))
print(m.as_string().splitlines()[:2])
print('module _fmt =', repr(getattr(G, '_fmt', None)))
