import sys, re, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
s.post(BASE + "signup", data={"username": "u752g", "email": "u752g@x.io", "password": "p752g"}, timeout=20)
time.sleep(0.5)
s.post(BASE + "login", data={"username": "u752g", "password": "p752g"}, timeout=20)
time.sleep(0.5)
added = 0
for i in range(6):
    try:
        r = s.post(BASE + "expenses", data={"description": "exp%d" % i, "amount": str(10 + i),
                                            "date": "2024-01-%02d" % (i + 1)}, timeout=25)
        added += 1
    except Exception as e:
        print("ajout %d ERR %s" % (i, type(e).__name__))
    time.sleep(1.0)
print("ajoutees:", added)
r = s.get(BASE + "expenses", timeout=25)
print("page:", len(r.text), "octets")
print("=== liens ===")
for m in re.finditer(r"href=\"([^\"]{1,80})\"", r.text):
    h = m.group(1)
    if "?" in h or h.startswith("/"):
        print("  ", h)
print("=== lignes ===")
for m in re.finditer(r"<td[^>]*>([^<]{0,25})</td>", r.text):
    print("  ", m.group(1).strip())
