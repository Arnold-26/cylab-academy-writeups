import sys, json, re, time, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

requests.packages.urllib3.disable_warnings()
cy = CyLab(delay=0.5)
cy.login()
B = pathlib.Path(r"/tmp/cylab_eps")
for attempt in range(3):
    cy.req("PUT", "/api/challenges/133/instance/?source=library")
    got = ""
    for i in range(6):
        st, b = cy.req("GET", "/api/challenges/133/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        desc = d.get("description") or ""
        if "challenge-files" in desc:
            got = desc
            break
        time.sleep(0.4)
    if got:
        print("=== desc avec liens ===")
        print(got[:600])
        for u in re.findall(r"https?://[^\s'\"<>]+", got):
            name = u.rsplit("/", 1)[-1]
            dest = B / f"133_{name}"
            if dest.exists() and dest.stat().st_size > 100:
                print("deja", dest.name, dest.stat().st_size)
                continue
            try:
                r = requests.get(u, timeout=90, verify=False)
                dest.write_bytes(r.content)
                print("ok", dest.name, len(r.content))
            except Exception as e:
                print("err", name, type(e).__name__)
        break
    print("essai %d: pas de liens" % (attempt + 1))
