import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
r = requests.get(BASE, timeout=20)
print(r.text)
print("\n=== POST simple avec identifiants bidon ===")
r2 = requests.post(BASE, data={"name": "admin", "pass": "admin"}, timeout=20)
print("status:", r2.status_code, "len:", len(r2.text))
for m in re.finditer(r"<div class=\"alert[^>]*>(.*?)</div>", r2.text, re.S):
    print("ALERT:", re.sub(r"\s+", " ", m.group(1))[:200])
