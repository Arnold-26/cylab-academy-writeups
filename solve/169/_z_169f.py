import sys, requests, urllib3, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
got = {}
for n in ("poeMD5_A.pdf", "poeMD5_B.pdf"):
    for sub in ("examples/", "examples/free/"):
        u = "https://raw.githubusercontent.com/corkami/collisions/master/" + sub + n
        try:
            r = requests.get(u, timeout=30, verify=False)
            if r.status_code == 200 and r.content[:4] == b"%PDF":
                got[n] = r.content
                open(B + "\\169_" + n, "wb").write(r.content)
                print("OK", sub + n, len(r.content))
                break
            else:
                print("--", sub + n, r.status_code)
        except Exception as e:
            print("--", sub + n, type(e).__name__)
if len(got) == 2:
    a = got["poeMD5_A.pdf"]; b = got["poeMD5_B.pdf"]
    ha = hashlib.md5(a).hexdigest(); hb = hashlib.md5(b).hexdigest()
    print("md5 A:", ha)
    print("md5 B:", hb)
    print("COLLISION:", ha == hb, "| differents:", a != b)
