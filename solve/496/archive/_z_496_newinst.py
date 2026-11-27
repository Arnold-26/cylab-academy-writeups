import sys, json
sys.path.insert(0, r'.')
from cylab2 import CyLab
cy = CyLab(delay=1.0)
cy.login()
st, b = cy.req('DELETE', '/api/challenges/496/instance/')
print('DEL', st)
import time; time.sleep(2)
st, b = cy.req('PUT', '/api/challenges/496/instance/?source=library')
print('PUT', st)
for i in range(20):
    time.sleep(3)
    st, b = cy.req('GET', '/api/challenges/496/instance/')
    d = json.loads(b)
    if d.get('status') == 'RUNNING':
        import re
        u = re.findall(r"href='([^']+)'", d.get('description') or '')
        print('URL', u[0] if u else None, 'expires', d.get('expires_in'))
        break
    print(i, d.get('status'))
