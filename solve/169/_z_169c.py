import sys, requests, urllib3, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
base = "https://raw.githubusercontent.com/corkami/collisions/master/examples/free/"
names = ["collision1.pdf", "collision2.pdf", "pdf1.pdf", "pdf2.pdf", "free/collision1.pdf"]
found = {}
for n in names:
    try:
        r = requests.get(base + n, timeout=25, verify=False)
        if r.status_code == 200 and r.content[:4] == b"%PDF":
            found[n] = r.content
            print("OK", n, len(r.content), hashlib.md5(r.content).hexdigest())
        else:
            print("--", n, r.status_code, r.content[:20])
    except Exception as e:
        print("--", n, type(e).__name__)
if len(found) >= 2:
    ks = list(found)[:2]
    a, b = found[ks[0]], found[ks[1]]
    print("md5 A:", hashlib.md5(a).hexdigest())
    print("md5 B:", hashlib.md5(b).hexdigest())
    print("identiques ?", a == b)
    open("/tmp/cylab_eps/169_a.pdf", "wb").write(a)
    open("/tmp/cylab_eps/169_b.pdf", "wb").write(b)
