import sys, tarfile, re, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

print("=== contenu complet du tarball 494 ===")
with tarfile.open(r"/tmp/cylab_eps\494_server.tar.gz") as t:
    for m in t.getmembers():
        print("  %-60s %s %d" % (m.name[:60], "D" if m.isdir() else "F", m.size))

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/478/instance/?source=library")
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/478/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    if desc:
        break
print("\n=== description 478 ===")
print(desc.replace("\n", " ")[:900])
print("\n=== urls ===")
for m in re.finditer(r"https?://[^\s'\"<>]+", desc):
    print("  ", m.group(0))
