import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
stored = bytes.fromhex("7b 7f 78 0f 06 75 15 3e 0f 1b 69 4e 0c 0f 78 39 3d 0a 11 7e 4d 3d 58 10 64 10 50 08 2a 3a 3b 01 10 2f 16 69 07 10 32 1f")
print("stored:", len(stored), stored.hex())

out = []
for i in range(len(stored)):
    v = stored[i]
    # annuler dans l'ordre inverse : i%3, i%2, i%10, i-3, i-1, puis 20
    if i % 3 == 0:
        v ^= 7
    elif i % 3 == 1:
        v ^= 6
    else:
        v ^= 5
    if i % 2 == 0:
        v ^= 9
    else:
        v ^= 8
    v ^= (i % 10)
    if i > 2:
        v ^= stored[i - 3]
    if i > 0:
        v ^= stored[i - 1]
    v ^= 20
    out.append(v & 0xFF)

s = bytes(out)
print("decode:", s)
try:
    print("ascii :", s.decode("utf-8", "replace"))
except Exception:
    pass

# soumission
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu
txt = s.decode("latin-1")
inner = txt
for pfx in ("academy{", "picoCTF{"):
    if txt.startswith(pfx):
        inner = txt[len(pfx):].rstrip("}")
cands = ["academy{%s}" % inner, txt, "picoCTF{%s}" % inner]
cy = CyLab(delay=1.0)
cy.login()
ok = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 182, "flag": c})
    try:
        o = json.loads(b).get("correct")
    except Exception:
        o = None
    print("182 <- %-50s -> %s" % (c, o))
    if o:
        ok = c
        break
print("FLAG:", ok)
