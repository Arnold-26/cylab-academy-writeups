import sys, requests, urllib3, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
base = "https://raw.githubusercontent.com/corkami/collisions/master/examples/free/"
B = r"/tmp/cylab_eps"
got = {}
for n in ("poeMD5_A.pdf", "poeMD5_B.pdf"):
    r = requests.get(base + n, timeout=30, verify=False)
    print(n, r.status_code, len(r.content), r.content[:4])
    if r.status_code == 200:
        got[n] = r.content
        open(B + "\\169_" + n, "wb").write(r.content)
if len(got) == 2:
    a = got["poeMD5_A.pdf"]; b = got["poeMD5_B.pdf"]
    ha = hashlib.md5(a).hexdigest(); hb = hashlib.md5(b).hexdigest()
    print("md5 A:", ha)
    print("md5 B:", hb)
    print("COLLISION:", ha == hb)
    print("contenus differents:", a != b)
