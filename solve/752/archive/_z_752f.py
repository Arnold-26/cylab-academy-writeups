import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
s.post(BASE + "signup", data={"username": "u752f", "email": "u752f@x.io", "password": "p752f"}, timeout=15)
s.post(BASE + "login", data={"username": "u752f", "password": "p752f"}, timeout=15)
for i in range(12):
    s.post(BASE + "expenses", data={"description": "exp%d" % i, "amount": str(10 + i), "date": "2024-01-%02d" % (i + 1)}, timeout=15)
r = s.get(BASE + "expenses", timeout=15)
print("=== pagination apres ajout ===")
for m in re.finditer(r"<a href=\"([^\"]*)\"[^>]*>.*?(chevron_left|chevron_right|\d+)", r.text, re.S):
    print("  ", m.group(1)[:80])
print("=== recherche de parametres de tri ===")
for m in re.finditer(r"(sort|order|order_by|page)=([^&\"']*)", r.text):
    print("  ", m.group(0)[:60])
print("=== lignes du tableau ===")
for m in re.finditer(r"<td[^>]*>([^<]{0,30})</td>", r.text):
    print("  ", m.group(1).strip())
