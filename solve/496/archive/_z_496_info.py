import sys, json, re
sys.path.insert(0, r'.')
from cylab2 import CyLab
cy = CyLab(delay=1.0)
cy.login()
st, b = cy.req('GET', '/api/challenges/496/instance/')
d = json.loads(b)
print(d.get('status'), d.get('expires_in'))
print(re.findall(r"href='([^']+)'", d.get('description') or ''))
